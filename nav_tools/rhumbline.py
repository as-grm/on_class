#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Feb 18 12:57:30 2022

@author: sandro@fpp.uni-lj.si

Rhumb line calculations!
"""

import sys
sys.path.append('../nav_tools')

import math as mat
import navtools as nt


# Calculates distance and course out of p0 and p1
# This is the first Loxodrome problem!
def rhumbLineP1(p0, p1):
    
    fi0r = nt.deg2rad(p0[0]);
    la0d = p0[1];
    fi1r = nt.deg2rad(p1[0]);
    la1d = p1[1];
    
    dfr = fi1r - fi0r; # delta LAT with sign
    dlr = nt.deg2rad(nt.deltaLong(la0d, la1d)) # delta lONG with sign
    
    # Calculation of tilde LAT (it will be always a positive number)
    if mat.fabs(dfr) < 1e-8: # Check if delta LAT = 0
        ft = 0
    else:
        c_ft = dfr/mat.log(mat.tan(mat.pi/4 + fi1r/2)/mat.tan(mat.pi/4 + fi0r/2))
        ft = mat.acos(c_ft)
        if c_ft < 0: # condition for negative angles (180 - ft)
            ft = mat.pi - ft
    #print('ft = {:.2f}'.format(ft*180/mat.pi))
    
    # Depature course. Result is always in I quadrant [0,90]
    if mat.fabs(dfr) < 1e-8:
        w = mat.pi/2
    else:
        w = mat.atan(mat.cos(ft)*mat.fabs(dlr/dfr))
    
    # Loxodrome distance
    if mat.fabs(dfr) < 1e-8:
        d = mat.fabs(dlr)*mat.cos(fi0r)
    elif mat.fabs(dlr) < 1e-8:
        d = mat.fabs(dfr)
    elif (mat.fabs(w) < mat.pi/20) or (mat.fabs(w - mat.pi) < mat.pi/20): # Condition to avoid small numbers
        d = mat.afbs(dfr)/mat.cos(w)
    else:
        d = mat.cos(ft)*mat.fabs(dlr)/mat.sin(w)
    
    wL = nt.rad2deg(nt.navAngle(w,dfr,dlr)) # Convert to real course in deg!
    dL = nt.rad2deg(d)*60 # convert to Nm!
    
    return [dL, wL]


# Calculates second position from first position, distance and angle
# This is the second loxodrome problem!
def rhumbLineP2(p0,dL,wL):

    fi0r = nt.deg2rad(p0[0])
    la0r = nt.deg2rad(p0[1])
    wLr = nt.deg2rad(wL)
    dr = nt.deg2rad(dL/60) # assume dL is in Nm!
    
    dfr = mat.fabs(dr * mat.cos(wLr))
    R = dr * mat.sin(wLr)
    
    # Find delta fi and fi1
    if (mat.fabs(wL) < 1e-8) or (mat.fabs(wL - 180.0) < 1e-8) or (mat.fabs(wL - 360.0) < 1e-8): # case dl = 0, on parallel
        fi1r = fi0r;
    elif (wL > 90.0) and (wL < 270.0):
        fi1r = fi0r - dfr
    else:
        fi1r = fi0r + dfr
    
    # Find delta la and la1 
    if (mat.fabs(wL) < 1e-8) or (mat.fabs(wL - 360.0) < 1e-8) or (mat.fabs(wL - 180.0) < 1e-8): # case df = 0, on meridian
        dlr = 0
    elif (mat.fabs(wL - 90.0) < 1e-8) or (mat.fabs(wL - 270.0) < 1e-8): # Check if w = 90, 270!
        dlr = mat.fabs(R/mat.cos(fi0r))
    else:
        cos_ft = dfr/mat.log(mat.tan(mat.pi/4 + fi1r/2)/mat.tan(mat.pi/4 + fi0r/2))
        dlr = mat.fabs(R/cos_ft)
    
    if (wLr < mat.pi):
        la1r = la0r + dlr
    else:
        la1r = la0r - dlr
    
    fi1 = nt.rad2deg(fi1r)
    la1 = nt.rad2deg(la1r)
    
    return [fi1, la1]



