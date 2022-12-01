from OSMPythonTools.nominatim import Nominatim
from OSMPythonTools.overpass import overpassQueryBuilder, Overpass
#https://overpass-turbo.eu/# для проверки квадрата
#https://habr.com/ru/company/vk/blog/591879/ язык разметки
#http://bboxfinder.com/#54.840143,83.099232,54.842943,83.103631 генератор квадрата

class RangeBox:
    def __init__(self, current_position):
        """current_position is a tuple of degree coordinates (a, b) where

            a - latitude
            b - longitude
        """

        __RANGE = 0.00117


        self.position = current_position
    
    def bbox(self) -> tuple:
        """ Returns a bound box. """
        box = [ self.position[0] - self.RANGE, 
                self.position[1] + self.RANGE, 
                self.position[0] + self.RANGE, 
                self.position[0] - self.RANGE]
        return box
        

#0.00117
# nominatim = Nominatim()
# areaID = nominatim.query([83.100483,54.840505,83.103755,54.842266]).areaId()

query = overpassQueryBuilder(bbox=[54.841470,83.101153,54.842415,83.102790],elementType='node', selector="shop", out='body')
print(query)
overpass = Overpass()
shops = overpass.query(query)
print(shops.toJSON())