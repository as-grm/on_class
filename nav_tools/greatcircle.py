#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Feb 19 15:30:59 2022

@author: sandro@fpp.uni-lj.si

Great circle calculations!
"""

import sys
sys.path.append('../nav_tools')

import math as mat
import numpy as np
import navtools as nt


# Calculates the midpoint longitude on orthodrome
def getMidpointLong(la_1d, dl_m):
    
    long_m = la_1d + dl_m 
            
    if long_m < -180.0: # pasing from W -> E date line
        #print('dl_i < -180: la={:f}'.format(360 + dl_i))
        long_m = 360 + long_m
    elif long_m > 180.0: # passing from E -> W date line
        #print('dl_i > 180: la={:f}'.format(dl_i - 360))
        long_m = long_m - 360
        
    return long_m


# Calculates first orthodrome parameters
# distance, departure course, vertex position
def getGCparameters(p0,p1):

    # Covert to radians
    fi0r = nt.deg2rad(p0[0])
    psi0r = mat.pi/2 - fi0r
    la0d = p0[1]
    fi1r = nt.deg2rad(p1[0])
    psi1r = mat.pi/2 - fi1r
    la1d = p1[1]
    
    dlar = nt.deg2rad( nt.deltaLong(la0d, la1d) )
    
    # Find distance
    cos_d = mat.cos(psi0r) * mat.cos(psi1r) + mat.sin(psi0r) * mat.sin(psi1r) * mat.cos(mat.fabs(dlar)); 
    dr = mat.acos(cos_d);
    d = nt.rad2deg(dr)*60; # distance in Nm
    
    # Find departure course
    w = mat.acos( (mat.cos(psi1r) - mat.cos(psi0r) * mat.cos(dr))/( mat.sin(psi0r) * mat.sin(dr)));
    if dlar < 0:
        w1 = 360 - nt.rad2deg(w)
    else:
        w1 = nt.rad2deg(w)
        
    # Vertex latitiude   
    fivr = np.sign(mat.cos(w)) * mat.acos( mat.fabs(mat.sin(w)) * mat.cos(fi0r) )
    fiv = nt.rad2deg(fivr)
    
    # Vertex longitude
    pivr = np.sign(dlar) * mat.acos( mat.tan(fi0r)/mat.tan(fivr))
    lav = getMidpointLong(la0d, nt.rad2deg(pivr))
    
    return [d,w1,[fiv,lav]]


# Get midpoint position on the orthdrome path
# Input for midpoit position is longitude in decimal degrees
def getMidPosition(P0,P1,la_md):
    
    [d_gc, w1_gc, [fiv_gc, lav_gc]] = getGCparameters(P0, P1)
    
    fi_0r = nt.deg2rad(P0[0])
    dla_d = nt.deltaLong(P0[1], P1[1])
    
    # convert W1_GC to original value
    if (dla_d < 0):
        w = nt.deg2rad(360.0 - w1_gc)
    else:
        w = nt.deg2rad(w1_gc)
    
    # find midpoint latitude using P_0 (stable)
    dla_mr = mat.fabs(nt.deg2rad(nt.deltaLong(P0[1], la_md)));
    if (fi_0r < 0):
        w = mat.pi - w
        fi_0r = mat.fabs(fi_0r)
        fi_mr = mat.atan( mat.sin(dla_mr) / (mat.tan(w) * mat.cos(fi_0r)) + mat.tan(fi_0r) * mat.cos(dla_mr) )
        fi_mr = - fi_mr
    else:
        fi_mr = mat.atan( mat.sin(dla_mr) / (mat.tan(w) * mat.cos(fi_0r)) + mat.tan(fi_0r) * mat.cos(dla_mr) );
    
    fi_md = nt.rad2deg(fi_mr)
    
    return fi_md


# Calculates set of midpoints on orthodrome path
# dla specifies delta lambda: normally 5,10 deg
def getPathPoints(P0,P1,dla=1):
    
    la_mps = nt.getPathPointsLong(P0[1], P1[1], dla)
    
    fi_mps = []
    for la in la_mps:
        fi_i = getMidPosition(P0, P1, la)
        fi_mps.append(fi_i)
        
    return np.transpose(np.array([fi_mps, la_mps]))


# Converts GC path to a piecewise RL lines
def convertGC2RL(P0,P1,dla):
    
    Pm = getMidPoints(P0, P1, dla)
    return np.concatenate(([P0],Pm,[P1]))
    