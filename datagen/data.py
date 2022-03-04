import pandas as pd
import random
from bokeh.sampledata.us_counties import data as counties

counties = {
    code: county for code, county in counties.items() if county["state"] in ("tx, la")
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

data.to_csv("geo_coded_us_counties.csv", index=False)


