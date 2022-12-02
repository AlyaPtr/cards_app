from math import acos, sin, cos, fabs, pi
from json import dumps



from OSMPythonTools.nominatim import Nominatim
from OSMPythonTools.overpass import overpassQueryBuilder, Overpass


_RANGE = 0.00117
_EARTH_RADIUS = 6371000
_PRIORITYCOUNT = 25


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

    def getData(self):
        return self.overpass.query(self.request()).toJSON()

class CollectedList:
    def __init__(self, current_possition):
        self.position = current_possition

        self.data = StoreList(RangeBox(self.position).get_box()).getData()
        
    def _distance(self, pos) -> float:
        """ Calculating distance between 2 points using Spherical law of cosines.

        Keyword arguments:
        pos -- is a tuple of latitude, longitude
        """
        lat1, lat2 = (self.position[0]*pi)/180, (pos[0]*pi)/180
        dLon = fabs((self.position[1]*pi)/180 - (pos[1]*pi)/180)

        d = acos(sin(lat1)*sin(lat2) + cos(lat1)*cos(lat2)*cos(dLon))*_EARTH_RADIUS
        return d
    
    def response(self):
        """Create response JSON(aka python dict from OSM data in format {name:distance})


        """
        new_data = dict()
        count = min(_PRIORITYCOUNT, len(self.data['elements']))
        for i in range(count):
            try:
                name = self.data['elements'][i]['tags']['name']
                degree = (self.data["elements"][i]["lat"], self.data["elements"][i]["lon"])
            except:
                continue

            new_data[name] = self._distance(degree)

        sorted(new_data, key= lambda value: value[1])    
        return new_data
        







def main():
    clst = CollectedList((54.83976, 83.09502))
    print(clst.response())
   
main()