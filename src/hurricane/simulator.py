import json
import navigator as nav
import random
import shapely.wkt as wkt
import socket

from bokeh.driving import linear
from confluent_kafka import Producer
from datagen import Source
from plotter import BokehGeoFigure
from shapely.geometry import Point, MultiPoint
from shapely.ops import nearest_points
from typing import Callable

class Config:
# Navigation parameters
  refresh: int = 3000
  incLow: int = 1
  incHigh: int = 10 
  average: int = 20
  high: int = 50
  extreme: int = 100
  startState: str = "TX"
  startCounty: str = "Jefferson"
  direction: [] = ["NW"]
  spillLayer1: [] = ["E"]
  spillLayer2: [] = ["S"]

# Kafka ingestion
  bootstrap: str = "204.236.149.139:9092"  
  topic: str = "demo_hurricane_metrics"
  
  
class Simulator:
  def __init__(self, geoMap: BokehGeoFigure, source: Source, config: Config):
    self.geoMap = geoMap
    self.source = source
    self.conf = config
    self.mainPath = []
    self.spillLayer1Path = []
    self.spillLayer2Path = []
    self.stop = False
    self.start()

# Setup Kafka
    self.kafka = Producer({ 
                   "bootstrap.servers": self.conf.bootstrap,
                   "client.id": socket.gethostname()
                 })

  def start(self):
    i = -1
    while True:
      try:
        i = self.source.data["name"].index(self.conf.startCounty, i + 1)
        if self.source.data["state"][i] == self.conf.startState:
          break
      except ValueError:
        i = 0
        break

    self.mainPath.append(i)
    self.geoMap.ds.data["hazard_metric"][i] = self.conf.extreme

  def next(self): 
    if self.stop:
      return

# Get the next closest centroid in the direction of interest
    curr = self.mainPath[len(self.mainPath) - 1]
    wktOrigin = wkt.loads(str(self.source.data["centroids"][curr]))
    exclude = self.mainPath[len(self.mainPath) - 1]
    neighbors = self.getPath(wktOrigin, self.conf.direction, exclude)
    if len(neighbors) == 0:
      self.stop = True
      return

    n = []
    for j in neighbors.keys():
      n.append(wkt.loads(j))

    destinations = MultiPoint(n)
    closest = nearest_points(wktOrigin, destinations)[1]
    i = neighbors[str(closest)]
    self.mainPath.append(i)

    curr = i

# Get the 'spillLayer1' in the direction of interest from the latest
# centroid identified above
    wktOrigin = wkt.loads(str(self.source.data["centroids"][curr]))
    exclude = self.spillLayer1Path[len(self.spillLayer1Path)-1] if len(self.spillLayer1Path) > 0 else -1
    neighbors = self.getPath(wktOrigin, self.conf.spillLayer1, exclude)
    if len(neighbors) == 0:
      return

    n = []
    for j in neighbors.keys():
      n.append(wkt.loads(j))

    destinations = MultiPoint(n)
    closest = nearest_points(wktOrigin, destinations)[1]
    i = neighbors[str(closest)]
    self.spillLayer1Path.append(i)

# Get the 'spillLayer2' in the direction of interest from the latest
    wktOrigin = wkt.loads(str(self.source.data["centroids"][curr]))
    exclude = self.spillLayer2Path[len(self.spillLayer2Path)-1] if len(self.spillLayer2Path) > 0 else -1
    neighbors = self.getPath(wktOrigin, self.conf.spillLayer2, exclude)
    if len(neighbors) == 0:
      return

    n = []
    for j in neighbors.keys():
      n.append(wkt.loads(j))

    destinations = MultiPoint(n)
    closest = nearest_points(wktOrigin, destinations)[1]
    i = neighbors[str(closest)]
    self.spillLayer2Path.append(i)

  def getPath(self, point: Point, direction: str, exclude: int) -> {}:
    neighbors = {}
    for i in range(self.source.numRecords):
      if i == exclude:
        continue
      wktDest = wkt.loads(str(self.source.data["centroids"][i]))
      xDest = wktDest.x
      yDest = wktDest.y
      compass, degrees = nav.direction(point.x, point.y, xDest, yDest)       
      if compass in direction:
        neighbors[str(wktDest)] = i
    return neighbors

  def sink(self) -> None:
    for i in range(self.source.numRecords):
      d = {  
            "us_state":         self.geoMap.ds.data["state"][i],  
            "us_county":        self.geoMap.ds.data["name"][i],  
            "hazard_metric":    self.geoMap.ds.data["hazard_metric"][i]
          }
      key = self.geoMap.ds.data["state"][i] + ":" + self.geoMap.ds.data["name"][i] 
      record = json.dumps(d)
      print(record)

#      self.kafka.produce(self.conf.topic, key=key, value=record)
#      self.kafka.flush()

  def getUpdate(self) -> Callable[[int], None]:
    @linear()
    def update(step):
      self.next()
      for i in range(self.source.numRecords):
        v = self.conf.average * (1 + random.randint(self.conf.incLow, self.conf.incHigh)/100) 
        self.geoMap.ds.data["hazard_metric"][i] = v

      for i in self.mainPath:
        v = self.conf.extreme * (1 + random.randint(self.conf.incLow, self.conf.incHigh)/100)
        self.geoMap.ds.data["hazard_metric"][i] = v

      for i in self.spillLayer1Path:
        v = self.conf.high * (1 + random.randint(self.conf.incLow, self.conf.incHigh)/100)
        self.geoMap.ds.data["hazard_metric"][i] = v

      for i in self.spillLayer2Path:
        v = self.conf.high * (1 + random.randint(self.conf.incLow, self.conf.incHigh)/100)
        self.geoMap.ds.data["hazard_metric"][i] = v

      self.sink()
      self.geoMap.ds.trigger("data", self.geoMap.ds.data, self.geoMap.ds.data)

    return update
     
