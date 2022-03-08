import datagen
import plotter as geo
import simulator 
import time
from bokeh.plotting import curdoc

data = datagen.BokehGeoFromFile("../data/geo_dataset.csv")
geoMap = geo.BokehGeoFigure(data.dictionary)
geoMap.createFigure()

conf = simulator.Config()
sim = simulator.Simulator(geoMap, data, conf)
update = sim.getUpdate()

curdoc().add_root(geoMap.p)
curdoc().plot_height = 800
curdoc().plot_width = 600
curdoc().add_periodic_callback(update, conf.refresh)
