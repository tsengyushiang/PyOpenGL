from math import *

def Spherical2Cartesian(rvh):
    r = rvh[0]
    v = radians(rvh[1])
    h = radians(rvh[2])
    
    return (r*sin(h)*cos(v), r*sin(h)*sin(v), r*cos(h))
