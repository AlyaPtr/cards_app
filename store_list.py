from math import acos, sin, cos, fabs, pi

from OSMPythonTools.nominatim import Nominatim
from OSMPythonTools.overpass import overpassQueryBuilder, Overpass



_RANGE = 0.00117
_EARTH_RADIUS = 6371000


#https://overpass-turbo.eu/# для проверки квадрата
#https://habr.com/ru/company/vk/blog/591879/ язык разметки
#http://bboxfinder.com/#54.840143,83.099232,54.842943,83.103631 генератор квадрата


"""
TODO:

Пересобрать полученный с OSM ответ в новый json+посчитать расстояния до разумного количества элементов

"""


class RangeBox:
    def __init__(self, current_position):
        """
            Keyword arguments:

            current_position -- is a tuple of degree coordinates (a, b) where
            a - latitude
            b - longitude

            Constants:
            RANGE -- special constant for calculate radius

        """

       


        self.position = current_position
    
    def get_box(self) -> list:
        """ Returns a bound box. """
        box = [ self.position[0] - _RANGE, 
                self.position[1] - _RANGE, 
                self.position[0] + _RANGE, 
                self.position[1] + _RANGE]
        return box
                
class StoreList:
    def __init__(self, bbox):   
        self.zone = bbox
        self.JSONS = []
        
        self.overpass = Overpass()

    def request(self):
        """ Request to OSM"""
        query = overpassQueryBuilder(
            bbox = self.zone,
            elementType = ['node'],
            selector = ['shop'],

        )
        return query

    def printJSON(self):
        return self.overpass.query(self.request()).toJSON()

class CollectedList:
    def __init__(self, current_possition, data):
        self.data = data
        self.position = current_possition
        
    def distance(self, pos) -> float:
        """ Calculating distance between 2 points using Spherical law of cosines.

        Keyword arguments:
        pos -- is a tuple of latitude, longitude
        """
        lat1, lat2 = (self.position[0]*pi)/180, (pos[0]*pi)/180
        dLon = fabs((self.position[1]*pi)/180 - (pos[1]*pi)/180)

        d = acos(sin(lat1)*sin(lat2) + cos(lat1)*cos(lat2)*cos(dLon))*_EARTH_RADIUS
        return d

#0.00117
# nominatim = Nominatim()
# areaID = nominatim.query([83.100483,54.840505,83.103755,54.842266]).areaId()

def main():
    testBox = RangeBox((54.841543,83.101431)).get_box()
    #print(testBox)
    lst = StoreList(testBox).printJSON()
    test = (lst["elements"][3]["lat"], lst["elements"][3]["lon"])
    print(lst["elements"][3]["lat"], lst["elements"][3]["lon"], sep =" ")
    clst = CollectedList((54.843, 83.0907), []).distance(test)
    print(clst)
    # query = overpassQueryBuilder(bbox=[54.841470,83.101153,54.842415,83.102790],elementType='node', selector="shop", out='body')
    # print(query)
    # overpass = Overpass()
    # shops = overpass.query(query)
    # print(shops.toJSON())
main()