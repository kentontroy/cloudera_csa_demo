import random
import data
from bokeh.driving import linear
from bokeh.io import show
from bokeh.models import LogColorMapper
from bokeh.palettes import Blues256 as blues256
from bokeh.plotting import figure, curdoc
from typing import Tuple

GEO = None

class BokehGeoFigure:
  def __init__(self, data: dict):
    self.data = data

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
                  fill_color={"field": "metrics", "transform": color_mapper},
                  fill_alpha=0.7, line_color="black", line_width=0.5)
    self.ds = r.data_source

    @property
    def counties(self) -> {}:
      pass
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

data = data.BokehGeoFromSamples("tx")
source = data.getDictionary()

GEO = BokehGeoFigure(source)
GEO.createFigure()
curdoc().add_root(GEO.p)
#curdoc().add_periodic_callback(update, 1000)


