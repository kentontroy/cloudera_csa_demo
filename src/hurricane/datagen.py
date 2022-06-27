import pandas as pd
import random
import shapely.wkt as wkt
from bokeh.sampledata.us_counties import data as counties
from shapely.algorithms.polylabel import polylabel
from shapely.errors import TopologicalError
from shapely.geometry import Point, Polygon
from typing import Protocol

class Source(Protocol):
  data: dict
  numRecords: int

class BokehGeoFromSamples:
  def __init__(self, states: str):
    self.counties = {
      code: county for code, county in counties.items() if county["state"] in (states)
    }
    county_xs = [county["lons"] for county in self.counties.values()]
    county_ys = [county["lats"] for county in self.counties.values()]
    county_names = [county["name"] for county in self.counties.values()]
    states = [county["state"] for county in self.counties.values()]
    hazard_metric = [0 for i in range(len(county_xs))]
    self.dictionary=dict(
      x=county_xs,
      y=county_ys,
      name=county_names,
      state=states,
      hazard_metric=hazard_metric,
    )
 
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
      f.write("state:county:polygon:centroid:isWithin:pole\n")
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
                                   county["state"].upper(),
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
    self.df = pd.read_csv(self.file, sep=":")
# county, state, polygon, centroid, isWithin, pole
    county_xs = []
    county_ys = []
    for p in self.df["polygon"].tolist():
       xs = []
       ys = []
       wktPoly = wkt.loads(str(p))
       coords = list(wktPoly.exterior.coords)
       for coord in coords:
         xs.append(coord[0])
         ys.append(coord[1])
       county_xs.append(xs)
       county_ys.append(ys)

    county_names = self.df["county"].tolist()	
    states = self.df["state"].tolist()
    centroids = self.df["centroid"].tolist()
    hazard_metric = [0 for i in range(len(county_xs))]
    self.dictionary=dict(
      x=county_xs,
      y=county_ys,
      name=county_names,
      state=states,
      centroids=centroids,  
      hazard_metric=hazard_metric,
    )

  @property
  def data(self) -> dict:
    return self.dictionary

  @property
  def numRecords(self) -> int:
    return self.df.shape[0]

def main():
  samples = BokehGeoFromSamples("tx, ok")
  samples.savePolygonsToFile("../data/geo_polygon_points.csv")
  samples.saveDataSetToFile("../data/geo_dataset.csv")

if __name__ == "__main__":
  main()
