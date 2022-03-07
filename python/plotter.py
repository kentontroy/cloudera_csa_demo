import random
from bokeh.io import show
from bokeh.models import LogColorMapper
from bokeh.palettes import Blues256 as blues256
from bokeh.plotting import figure
from typing import Tuple

class BokehGeoFigure:
  def __init__(self, data: dict):
    self.data = data

  def createFigure(self):
    TOOLS = "pan,wheel_zoom,reset,hover,save"
    palette = tuple(blues256)
    color_mapper = LogColorMapper(palette=palette)
    self.p = figure(
    	       title="Realtime Precipitation Analysis", tools=TOOLS,
    	       x_axis_location=None, y_axis_location=None,
    	       tooltips=[
                 ("Name", "@name"), ("Rainfall", "@hazard_metric%"), ("(Long, Lat)", "($x, $y)")
    	     ])
    self.p.grid.grid_line_color = None
    self.p.hover.point_policy = "follow_mouse"
    r = self.p.patches("x", "y", source=self.data,
                  fill_color={"field": "hazard_metric", "transform": color_mapper},
                  fill_alpha=0.7, line_color="black", line_width=0.5)
    self.ds = r.data_source


