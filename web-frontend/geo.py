
import random
from bokeh.driving import linear
from bokeh.io import show
from bokeh.models import LogColorMapper
from bokeh.palettes import Blues256 as palette
from bokeh.plotting import figure, curdoc
from bokeh.sampledata.unemployment import data as unemployment
from bokeh.sampledata.us_counties import data as counties

counties = {
    code: county for code, county in counties.items() if county["state"] in ("la, tx")
}

county_xs = [county["lons"] for county in counties.values()]
county_ys = [county["lats"] for county in counties.values()]
county_names = [county["name"] for county in counties.values()]
county_rates = [unemployment[county_id] for county_id in counties]

data=dict(
    x=county_xs,
    y=county_ys,
    name=county_names,
    rate=county_rates,
)

TOOLS = "pan,wheel_zoom,reset,hover,save"

palette = tuple(reversed(palette))
color_mapper = LogColorMapper(palette=palette)

p = figure(
    	title="Realtime Precipitation Analysis", tools=TOOLS,
    	x_axis_location=None, y_axis_location=None,
    	tooltips=[
        	("Name", "@name"), ("Rainfall", "@rate%"), ("(Long, Lat)", "($x, $y)")
    	])
p.grid.grid_line_color = None
p.hover.point_policy = "follow_mouse"

# GeoJSON describes points, lines and polygons (called Patches in Bokeh)
# A patch is a list of lists rather a vector of values
r = p.patches("x", "y", source=data,
          fill_color={"field": "rate", "transform": color_mapper},
          fill_alpha=0.7, line_color="black", line_width=0.5)

ds = r.data_source

@linear()
def update(step):
  ds.data["rate"] = [unemployment[county_id] * (1 + random.randint(0, 100) / 100) for county_id in counties]
  ds.trigger("data", ds.data, ds.data)
  
curdoc().add_root(p)

# Add a periodic callback to be run every 1000 milliseconds
curdoc().add_periodic_callback(update, 1000)


