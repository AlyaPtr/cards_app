from OSMPythonTools.nominatim import Nominatim
from OSMPythonTools.overpass import overpassQueryBuilder, Overpass

nominatim = Nominatim()
areaID = nominatim.query([83.100483,54.840505,83.103755,54.842266]).areaId()

query = overpassQueryBuilder(bbox=[54.840143,83.099232,54.842943,83.103631],elementType='node', selector="shop", out='body')
print(query)
overpass = Overpass()
shops = overpass.query(query)
print(shops.toJSON())