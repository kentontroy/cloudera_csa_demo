import random
from bokeh.driving import linear
from bokeh.io import show
from bokeh.models import LogColorMapper
from bokeh.palettes import Blues256 as blues256
from bokeh.plotting import figure, curdoc
from bokeh.sampledata.unemployment import data as unemployment
from bokeh.sampledata.us_counties import data as counties
from typing import Tuple

GEO = None

class BokehGeoFigure:
  def __init__(self, states: str):
    self.counties = {
      code: county for code, county in counties.items() if county["state"] in (states)
    }
    county_xs = [county["lons"] for county in self.counties.values()]
    county_ys = [county["lats"] for county in self.counties.values()]
    county_names = [county["name"] for county in self.counties.values()]
    county_rates = [unemployment[county_id] for county_id in self.counties]
    self.data=dict(
      x=county_xs,
      y=county_ys,
      name=county_names,
      rate=county_rates,
    )

  def createFigure(self):
    TOOLS = "pan,wheel_zoom,reset,hover,save"
    palette = tuple(reversed(blues256))
    color_mapper = LogColorMapper(palette=palette)
    self.p = figure(
    	       title="Realtime Precipitation Analysis", tools=TOOLS,
    	       x_axis_location=None, y_axis_location=None,
    	       tooltips=[
                 ("Name", "@name"), ("Rainfall", "@rate%"), ("(Long, Lat)", "($x, $y)")
    	     ])
    self.p.grid.grid_line_color = None
    self.p.hover.point_policy = "follow_mouse"
    r = self.p.patches("x", "y", source=self.data,
                  fill_color={"field": "rate", "transform": color_mapper},
                  fill_alpha=0.7, line_color="black", line_width=0.5)
    self.ds = r.data_source

    @property
    def counties(self) -> {}:
      return self.counties
    @property
    def data(self) -> dict:
      return self.data
    @property
    def p(self) -> object:
      return self.p
    @property
    def ds(self) -> object:
      return self.ds

@linear()
def update(step):
  GEO.ds.data["rate"] = [unemployment[county_id] * (1 + random.randint(0, 100) / 100) for county_id in GEO.counties]
  GEO.ds.trigger("data", GEO.ds.data, GEO.ds.data)

GEO = BokehGeoFigure("tx")
GEO.createFigure()
curdoc().add_root(GEO.p)
curdoc().add_periodic_callback(update, 1000)


