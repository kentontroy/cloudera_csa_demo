import pandas as pd
from bokeh.sampledata.us_counties import data as counties
from shapely.algorithms.polylabel import polylabel
from shapely.errors import TopologicalError
from shapely.geometry import Point, Polygon

counties = {
    code: county for code, county in counties.items() if county["state"] in ("tx")
}

data = None

i = 0
for county in counties.values():
  flattenedState = [county["state"].upper() for i in range(len(county["lons"]))]
  flattenedName =  [county["name"] for i in range(len(county["lons"]))]
  df = pd.DataFrame(
	 zip(county["lons"], county["lats"], flattenedState, flattenedName),
	 columns=["lon", "lat", "state", "county"])	
  if i == 0:
    data = df
  else:
    data = pd.concat([data, df], ignore_index=True, axis=0)
  i += 1

data.to_csv("geo_polygon_points.csv", index=False)

with open("geo_centroid_points.csv", "w") as f:
  f.write("county:polygon:centroid:isWithin:pole\n")
  for county in counties.values():
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
