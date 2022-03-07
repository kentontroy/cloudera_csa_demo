import random
from bokeh.driving import linear
from datagen import Source
from plotter import BokehGeoFigure

class Simulator:
  def __init__(self, geoMap: BokehGeoFigure, source: Source):
    self.geoMap = geoMap
    self.source = source

  def getUpdate(self):
    @linear()
    def update(step):
      self.geoMap.ds.data["hazard_metric"] = [ 
        random.randint(5, 10) for i in range(self.source.numRecords)
      ]
      self.geoMap.ds.trigger("data", self.geoMap.ds.data, self.geoMap.ds.data)
    return update
     
