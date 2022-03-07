import datagen
import plotter as geo
import simulator 
from bokeh.plotting import curdoc

data = datagen.BokehGeoFromFile("data/geo_dataset.csv")
source = data.dictionary

geoMap = geo.BokehGeoFigure(source)
geoMap.createFigure()

curdoc().add_root(geoMap.p)

sim = simulator.Simulator(geoMap, data)
update = sim.getUpdate()
curdoc().add_periodic_callback(update, 1000)
