import math
import pandas as pd
import shapely.wkt as wkt
from bokeh.sampledata.us_counties import data as counties
from bokeh.sampledata.unemployment import data as unemployment
from shapely.algorithms.polylabel import polylabel
from shapely.errors import TopologicalError
from shapely.geometry import Point, Polygon
from typing import Tuple

class BokehGeoFromSamples:
  def __init__(self, states: str):
    self.counties = {
      code: county for code, county in counties.items() if county["state"] in (states)
    }

  def getDictionary(self) -> dict:
    county_xs = [county["lons"] for county in self.counties.values()]
    county_ys = [county["lats"] for county in self.counties.values()]
    county_names = [county["name"] for county in self.counties.values()]
    county_initial_metrics = [unemployment[county_id] for county_id in self.counties]
    data=dict(
      x=county_xs,
      y=county_ys,
      name=county_names,
      metrics=county_initial_metrics,
    )
    return data

  def savePolygonsToFile(self, file: str) -> None:
    data = None
    i = 0
    for county in self.counties.values():
      flattenedState = [county["state"].upper() for i in range(len(county["lons"]))]
      flattenedName =  [county["name"] for i in range(len(county["lons"]))]
      df = pd.DataFrame(
	     zip(county["lons"], county["lats"], flattenedState, flattenedName),
	     columns=["lon", "lat", "state", "county"]
           )	
      if i == 0:
        data = df
      else:
        data = pd.concat([data, df], ignore_index=True, axis=0)
      i += 1

    data.to_csv(file, index=False)

  def saveDataSetToFile(self, file: str) -> None:
    with open(file, "w") as f:
      f.write("county:polygon:centroid:isWithin:pole\n")
      for county in self.counties.values():
        pts = []
        for i in range(len(county["lons"])): 
          pts.append(Point(county["lons"][i], county["lats"][i]))

        poly = Polygon(pts)
        pole = ""
        try:
          pole = polylabel(poly, tolerance=10)
        except TopologicalError:
          pole = "N/A"

        msg = "{0}:{1}:{2}:{3}:{4}".format(
                                   county["name"], 
                                   poly,
                                   poly.centroid, 
                                   poly.centroid.within(poly),
                                   pole
                                 )
        f.write(msg)
        f.write("\n")

class BokehGeoFromFile:
  def __init__(self, file: str):
    self.file = file

  def readDataSet(self) -> None:
# county, polygon, centroid, isWithin, pole
    self.df = pd.read_csv(self.file, sep=":")
	  
        #wktPoly = wkt.loads(str(poly))
        #coords = list(wktPoly.exterior.coords)
        #print(coords)
        #print("\n")

  def getDictionary(self) -> dict:
    pass

def direction(lonOrigin: float, latOrigin: float, 
              lonDest: float, latDest: float) -> Tuple[str, float]:
  compass = ["N", "NE", "E", "SE", "S", "SW", "W", "NW", "N"]
  deltaLon = lonDest - lonOrigin
  deltaLat = latDest - latOrigin
  degrees = math.atan2(deltaLon, deltaLat) / math.pi * 180
  if degrees < 0: 
    degrees = degrees + 360
  return compass[round(degrees / 45)], degrees

def main():
  samples = BokehGeoFromSamples("tx")
  samples.savePolygonsToFile("geo_polygon_points.csv")
  samples.saveDataSetToFile("geo_dataset.csv")

  file = BokehGeoFromFile("geo_dataset.csv")
  file.readDataSet()

  print(direction(2, 3, -2, -1))

if __name__ == "__main__":
  main()


