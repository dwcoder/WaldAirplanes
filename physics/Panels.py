import json

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.collections import PolyCollection
import matplotlib as mpl

import json
from pprint import pprint as pp

from shapely.geometry import Point as sgPoint
from shapely.geometry.polygon import Polygon as sgPolygon


def generate_point(center=(0,0), radius=1):
    #https://stackoverflow.com/questions/5837572/generate-a-random-point-within-a-circle-uniformly
    rand1, rand2, rand3 = np.random.random_sample(3)
    theta = rand1*np.pi*2
    u = rand2 + rand3
    u = u if u < 1 else 2-u
    x, y = (radius * u * np.cos(theta), radius * u * np.sin(theta))
    return x, y


class Error(Exception):
    pass

class PolygonError(Exception):
    pass

class panel(object):
    def __init__(self, polygon, name=""):
        self.name = name

        # This is the reference polygon for the shape
        # We won't update this, unless we have to
        self.__set_ref_polygon(self.cleanpolygon(polygon))

        self.current_loc_x = 0
        self.current_loc_y = 0
        self.current_rotation = 0

    def __set_ref_polygon(self, newpolygon):
        self.__polygon = self.cleanpolygon(newpolygon)
        self.__sgpolygon = sgPolygon(self.__polygon)
        self.__current = self.__polygon

    def setname(self, name):
        self.name = name

    def cleanpolygon(self, polygon):
        if isinstance(polygon, list):
            # Assume we got a 2 dimensional list, make it an array
            polygon = np.array(polygon)
        shape = polygon.shape
        if (len(shape) < 2) or (shape[0] < 3) or (shape[1] != 2 ):
            raise PolygonError('Polygon must have shape Nx2 with N >= 3')

        # If no issues, then we can return the polygon
        return polygon

    def __repr__(self):
        return str(self.__polygon)

    def gethomopoly(self, poly):
        x = poly
        ret = np.concatenate([x, np.ones((x.shape[0],1))] ,axis=1)
        return ret

    def nohomopoly(self, homopoly):
        ret = homopoly[:,0:2]
        return ret

    def getpoly(self):
        return self.__polygon

    def translate(self, poly, x, y):
        tt = np.array(
            [[  1 , 0  ,   x ],
            [   0 , 1  ,   y ],
            [   0 , 0  , 1     ]]
            )
        newpoly = self.gethomopoly(poly)
        newpoly = np.matmul(newpoly, tt.transpose())
        newpoly = self.nohomopoly(newpoly)

        return newpoly

    def rotate(self, poly, theta):
        tt = np.array(
            [[ np.cos(theta)   , -np.sin(theta) , 0],
            [  np.sin(theta)  , np.cos(theta) ,  0],
            [ 0, 0, 1]]
            )

        newpoly = self.gethomopoly(poly)
        newpoly = np.matmul(newpoly, tt.transpose())
        newpoly = self.nohomopoly(newpoly)
        return newpoly

    def update_ref_poly_rotate(self, theta):
        self.__set_ref_polygon(self.rotate(self.__polygon,theta))

    def update_ref_poly_translate(self, x, y):
        self.__set_ref_polygon(self.translate(self.__polygon,x, y))

    def set_location(self, x, y):
        self.current_loc_x = x
        self.current_loc_y = y
        self.calcualte_and_set_current()

    def set_rotation(self, theta):
        self.current_rotation = theta
        self.calcualte_and_set_current()

    def contains_point(self, x, y):
        maybe_contains = self.quick_check_contains_point(x, y)
        if not maybe_contains:
            return False
        else:
            return self.expensive_check_contains_point(x,y)

    def current_contains_point(self, x, y):
        maybe_contains = self.quick_check_current_contains_point(x, y)
        if not maybe_contains:
            return False
        else:
            return self.expensive_check_current_contains_point(x,y)

    def expensive_check_contains_point(self, x, y):
        sgpoint = sgPoint(x, y)
        return self.__sgpolygon.contains(sgpoint)

    def expensive_check_current_contains_point(self, x, y):
        sgpoint = sgPoint(x, y)
        sgpolygon = sgPolygon(self.current())
        return sgpolygon.contains(sgpoint)

    def quick_check_contains_point(self, x, y):
        """
        Do a quick check
        If this function returns true it may contain the point.
        """
        x_min = np.min(self.__polygon[:,0])
        x_max = np.max(self.__polygon[:,0])
        y_min = np.min(self.__polygon[:,1])
        y_max = np.max(self.__polygon[:,1])
        if (x < x_min) or (x > x_max):
            return False
        if (y < y_min) or (y > y_may):
            return False
        return True

    def quick_check_current_contains_point(self, x, y):
        """
        Do a quick check
        If this function returns true it may contain the point.
        """
        x_min = np.min(self.current()[:,0])
        x_max = np.max(self.current()[:,0])
        y_min = np.min(self.current()[:,1])
        y_max = np.max(self.current()[:,1])
        if (x < x_min) or (x > x_max):
            return False
        if (y < y_min) or (y > y_max):
            return False
        return True


    def calcualte_and_set_current(self):
        ref_poly = self.__polygon

        #always rotate first, then translate
        rotated = self.rotate(ref_poly,
                              self.current_rotation)
        rotated_and_translated = self.translate(rotated,
                                    self.current_loc_x,
                                    self.current_loc_y)

        self.__current = rotated_and_translated

    def current(self):
        return self.__current


class plane(object):
    def __init__(self, list_of_polys=None, list_of_panels=None):
        if list_of_polys is not None:
            self.__panels = [panel(poly) for poly in list_of_polys]

        self.current_loc_x = 0
        self.current_loc_y = 0

        self.current_rotation = 0

    def fix_ref_location(self, x, y):
        """This should only be run once.
        Ensure the midpoint of the plane is at 0,0
        """
        for pan in self.__panels:
            pan.update_ref_poly_translate(x,y)

    def fix_ref_rotation(self, theta):
        """This should only be run once.
        Ensure the plane is looking the right direction
        """
        for pan in self.__panels:
            pan.update_ref_poly_rotate(theta)

    def getpolys(self):
        return [x.getpoly() for x in self.__panels]

    def set_panels_location(self):
        for pan in self.__panels:
            pan.set_location( self.current_loc_x, self.current_loc_y)

    def set_panels_rotation(self):
        for pan in self.__panels:
            pan.set_rotation(self.current_rotation)

    def update_location(self, x_change, y_change):
        self.current_loc_x += x_change
        self.current_loc_y += y_change
        self.set_panels_location()

    def update_rotation(self, theta_change):
        self.current_rotation += theta_change
        self.set_panels_rotation()


    def move_forward(self, units):
        theta = self.current_rotation
        x_change = units*np.cos(theta)
        y_change = units*np.sin(theta)

        self.update_location( x_change, y_change)

    def current(self):
        list_of_polys = [pan.current() for pan in self.__panels]

        return list_of_polys

    def contains_point(self, x, y):
        list_bool = [pan.contains_point(x, y) for pan in self.__panels]
        return any(list_bool)

    def __panels_contain_point(self, x, y):
        list_bool = [pan.current_contains_point(x, y) for pan in self.__panels]
        return list_bool

    def current_contains_point(self, x, y):
        list_bool = self.__panels_contain_point(x, y)
        return any(list_bool)


    def calculate_damage_of_shot(self, x, y):
        critical_points = np.array(
            [[-15,40],
            [15, 40]])

        exp_decay = 1.0/10.0

        hit = self.current_contains_point(x, y)
        if not hit:
            return 0
        if hit:
            hitpoint = np.array([x,y])
            distances = [np.linalg.norm(hitpoint - crit) for crit in critical_points]
            min_dist = min(distances)

            damage = np.exp(-min_dist * exp_decay)
            return(damage)







