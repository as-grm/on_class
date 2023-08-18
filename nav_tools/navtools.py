#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Feb 18 12:57:30 2022

@author: sandro@fpp.uni-lj.si

File containing Navigation programming tools!
"""

import math as mat
import numpy as np
import mpl_toolkits.basemap as bmap
import matplotlib.pyplot as mpl
mpl.rcParams['text.usetex'] = True
mpl.rcParams.update({'font.size': 7})

# print in arc text
arc_deg = u'\N{DEGREE SIGN}'
arc_min = u'\N{PRIME}'
long_minus = '\u2212'
u_varphi = '\u03C6'
u_lambda = '\u03BB'
u_omega = '\u03C9'


# Pretty print of degrees minutes form
def prettyPrintDM(x,z):
    
    x = mat.fabs(x)
    x_d = mat.floor(x)
    x_m = (x - x_d)*60.0
    
    if (60.0 - x_m) < 1e-5:
        x_d += 1
        x_m = 0.0
    
    if z == 3:
        fmt_str = '{:03d}{:s}{:05.2f}{:s}'.format(x_d,arc_deg,x_m,arc_min)
    else:
        fmt_str = '{:02d}{:s}{:05.2f}{:s}'.format(x_d,arc_deg,x_m,arc_min)
    
    return fmt_str

    
# Pretty print of position coordinate
def prettyPrintPos(x,o,z):
    
    dm_str = prettyPrintDM(x,z)
    fmt_str = '{:s}{:s}'.format(dm_str,o)
    
    return fmt_str


# Pretty print of latitude
def prettyPrintLat(x):
    
    if x > 0:
        o = 'N'
    else:
        o = 'S'
        
    return prettyPrintPos(x,o,2)


# Pretty print of longitude
def prettyPrintLong(x):
    
    if x > 0:
        o = 'E'
    else:
        o = 'W'
        
    return prettyPrintPos(x,o,3)


# Pretty print of Hour angle
def prettyPrintHA(x):
    
    return prettyPrintDM(x,3)


# Pretty print of declination
def prettyPrintDec(x):
    
    return prettyPrintLat(x)


# Pretty print of altitude
def prettyPrintAlt(x):
    
    x_sgn = np.sign(x)
    x = mat.fabs(x)
    x_d = mat.floor(x)
    x_m = (x - x_d)*60.0
    
    if (60.0 - x_m) < 1e-5:
        x_d += 1
        x_m = 0.0
    
    if x_sgn > 0.0:
        fmt_str = '{:02d}{:s}{:05.2f}{:s}'.format(x_d,arc_deg,x_m,arc_min)
    else:
        fmt_str = '-{:02d}{:s}{:05.2f}{:s}'.format(x_d,arc_deg,x_m,arc_min)
    
    return fmt_str
    
    return prettyPrintDM(x,2)


# Pretty print of azimuth
def prettyPrintAz(x):
    
    return '{:06.2f}{:s}'.format(x,arc_deg)


# Print position of decimal degree coordinates
def getPositionString(p):
    
    fi = p[0]
    la = p[1]
    
    return printPosition(fi, la)
    
# Print position of decimal degree coordinates
def printPosition(fi, la):
      
    fi_str = prettyPrintLat(fi)
    la_str = prettyPrintLong(la)
        
    return '{:s}={:s}; {:s}={:s}'.format(u_varphi, fi_str, u_lambda, la_str)

# Converts angle specified in degrees, minutes and seconds in decimal degrees
def dms2dd(x):
    
    sgn = np.sign(x[0])
    if len(x) == 2:
        return sgn*( mat.fabs(x[0]) + mat.fabs(x[1])/60.0)
    elif len(x) == 3:
        return sgn*( mat.fabs(x[0]) + mat.fabs(x[1])/60.0 + mat.fabs(x[2])/3600.0)
    else:
        print('Input size mismatch: len(x)={:d}'.format(len(x)))
        raise AssertionError()


# Converts angle specified in decimal degrees to degrees, minutes and seconds in decimal degrees
def dd2dms(x, ss=False):
    
    sgn = np.sign(x)
    x = mat.fabs(x)
    dd = mat.floor(x)
    if ss:
        mm = mat.floor((x-dd)*60)
        ss = (x - dd - mm/60)*60
    else:
        mm = (x-dd)*60
        ss = 0
    
    return [sgn*dd, mm, ss]
    
# Converts navigational format to decimal degree format
def nav2dd(x):
    
    nn = len(x)
    if nn != 3:
        print('Strange position format: {:}'.format(x))
        raise AssertionError()
    
    d = x[0]
    m = x[1]
    o = x[2]
    
    if (o == 'S') or (o == 'W'):
        d = -d
    elif (o == 'N') or (o == 'E'):
        d = d
    else:
        print('Wrong position orientation: {:}'.format(o))
        raise AssertionError()
        
    return dms2dd([d,m])


# Converts decimal degrees in radians
def deg2rad(dd):
    
    return dd/180.0*mat.pi


# Converts radians to decimal degrees
def rad2deg(rr):
    
    return rr/mat.pi*180.0


# Calculates delta LONG in a correct way
# All calculations are orineted westward 0...360 as hour angles!
def deltaLong(la0, la1):

    if la0 < 0:
        la0 = 360 + la0
    
    if la1 < 0:
        la1 = 360 + la1
    
    dl = la1 - la0;
    
    if dl < -180:
        dl = 360 + dl
    elif dl > 180:
        dl = dl - 360
        
    return dl


# Converts nautical angle to math angle
def mathAngle(c):
    
    if c > 0 and c <= mat.pi/2:
        w = mat.pi/2 - c
    elif c > mat.pi/2 and c <= 3*mat.pi/2:
        w = mat.pi/2 - c
    else:
        w = 2*mat.pi - c + mat.pi/2
    
    return w


# Finds navigational angle from mathematical angle
def navAngle(w, df, dl):
    
    if mat.fabs(df) < 1e-8: # df = 0
        if dl > 0:
            c = mat.pi/2;
        else:
            c = 3*mat.pi/2;
    elif mat.fabs(dl) < 1e-8: # dl = 0
        if df > 0:
            c = 0
        else:
            c = mat.pi;
    elif (df > 0) and (dl > 0): # I quadrant
        c = w
    elif (df < 0) and (dl > 0): # II quadrant
        c = mat.pi - w
    elif (df < 0) and (dl < 0): # III quadrant
        c = mat.pi + w
    else: # IV quadrant
        c = 2*mat.pi - w
    
    return c

# Convert position list to position numpy array
def position2array(pts):
    
    nn = len(pts)
    if nn < 2:
        print('Input size mismatch: len(pts)={:d}'.format(len(pts)))
        raise AssertionError()
        
    pa = np.zeros((nn,2))
    for i in range(nn):
        pa[i,0] = pts[i][0]
        pa[i,1] = pts[i][1]
        
    return pa

# Find crossing point of 180/-180 parallel
def getCrossingPoints(la_0, la_end, dla):
    
    if la_end > 180:
        k=0
        lt = la_0
        while lt < 180:
            k += 1
            lt = la_0 + k*dla
        la_c1 = lt - dla
        la_c2 = lt - 360
    else: # la_end < 180
        k=0
        lt = la_0
        while lt > -180:
            k += 1
            lt = la_0 - k*dla
        la_c1 = lt + dla
        la_c2 = 360 + lt
    
    return [la_c1, la_c2]
    

# Find midpoints in longitude range
def getMidpoints(la_0, la_1, dla):
    
    dls = np.sign(deltaLong(la_0, la_1))
    mpa = []
    
    if dls > 0:
        la_s = mat.ceil(la_0)
        dla_s = mat.fabs(mat.fmod(la_s, dla))

        if (dla - dla_s) < dla/2:
            la_s = la_s + 2*dla - dla_s
        else:
            la_s = la_s + dla - dla_s      
    else:
        la_s = mat.floor(la_0)
        dla_s = mat.fabs(mat.fmod(la_s, dla))

        if (dla - dla_s) < dla/2:
            la_s = la_s - 2*dla + dla_s
        else:
            la_s = la_s - dla + dla_s  
    
    #print('la_0:', la_0)
    #print('la_s:', la_s)
    
    mpa.append(la_0)
    
    k=0
    while True:
        mpa.append(la_s + k*dls*dla)
        k += 1
        la_tmp = la_s + k*dls*dla
        
        if dls > 0:
            if la_tmp > la_1: break
        if dls < 0:
            if la_tmp < la_1: break
    
    if la_1 != mpa[-1]:
        mpa.append(la_1)
    
    return np.array(mpa)    

# Find midpoints in longitude range
def getPathPointsLong(la_0, la_1, dla):
    
    dl = deltaLong(la_0, la_1)
    dls = np.sign(deltaLong(la_0, la_1))
    la_end = la_0 + dl
    
    if dl > 0:
        la_s = mat.ceil(la_0)
    else:
        la_s = mat.floor(la_0)
    
    if (la_end > 180) or (la_end < 180):
        if dl > 0:
            [la_c1, la_c2] = [180, -180+dla] #getCrossingPoints(la_s, la_end, dla)
        else:
            [la_c1, la_c2] = [-180, 180-dla]
            
        mps_1 = getMidpoints(la_0, la_c1, dla)
        mps_2 = getMidpoints(la_c2, la_1, dla)
        mps = np.concatenate((mps_1, mps_2), axis=None) 
        
    else:
        mps = getMidpoints(la_0, la_1, dla) 
    
    #print(mps)
    if np.abs(mps[-2] - mps[-1]) < dla/2:
        np.delete(mps, -2)
        
    if np.abs(mps[0] - mps[1]) < dla/2:
        np.delete(mps, 1)
    #print(mps)
    
    return mps
        
        
        
    
# Calculates the route central point
def getRouteCentralPoint(fi, la):
    
    # middle latitude
    fi_mid = (fi[0] + fi[1])/2
            
    # middle longitude
    dl = deltaLong(la[0], la[1])
    la_mid = la[0] + dl/2
    
    if la_mid > 180:
        la_mid = -180 + (la_mid - 180)
    elif la_mid < -180:
        la_mid = 180 + (la_mid + 180)
    
    return [fi_mid, la_mid]
        

# Plot Mercator chart and path
def plotPath(pts, dfi=5, dla=10, projection='merc', show_mid_pts=False, file_name=None, pv=None):

    nn = len(pts)
    if nn < 2:
        print('Input size mismatch: len(pts)={:d}'.format(len(pts)))
        raise AssertionError()

    fi = np.transpose(pts)[0]
    la = np.transpose(pts)[1]
    
    la_l = []
    for l in la:
        if l < 0:
            la_l.append(360 + l)
        else:
            la_l.append(l)
    la_l = np.array(la_l)
        
    if la_l[0] > la_l[-1]:
        fi_l = np.flip(fi)
        la_l = np.flip(la_l)
    
    fi_min = np.floor(np.min(fi_l))
    fi_min = fi_min - (fi_min%dfi)
    fi_max = np.ceil(np.max(fi_l))
    fi_max = fi_max + (dfi - fi_max%dfi)
    la_min = np.floor(np.min(la_l))
    la_min = la_min - (la_min%dla)
    la_max = np.ceil(np.max(la_l))
    la_max = la_max + (dla - la_max%dla)
    
    #print('la_min:', la_min, 'la_max:', la_max)
        
    fi_mid = (fi_min + fi_max)/2
    la_mid = (la_min + la_max)/2
    
    #print('BB: ({:},{:}) - ({:},{:})'.format(fi_min,la_min,fi_max,la_max))
    
    if projection == 'ortho':
        map = bmap.Basemap(projection='ortho',
            lat_0 = fi_mid,
            lon_0 = la_mid,
            resolution='l') #c croud par defaut, l low , h high , f full
        
    else:
        map = bmap.Basemap(projection='merc',
            lat_0 = fi_mid,
            lon_0 = la_mid,
            llcrnrlat = fi_min - 5, # lower left corner
            llcrnrlon = la_min - 1,
            urcrnrlat = fi_max + 5,  # upper right corner
            urcrnrlon = la_max + 1,
            resolution='l') #c croud par defaut, l low , h high , f full
        
        
    parallels = np.arange(fi_min, fi_max+1,dfi)
    meridians = np.arange(la_min, la_max+1, dla)
    #print('p:', parallels)
    #print('m:', meridians)
    
    if projection == 'ortho':
        map.drawparallels(parallels, linewidth=0.15)
        map.drawmeridians(meridians, linewidth=0.15)
    else:
        map.drawparallels(parallels, linewidth=0.15, labels=[True,False,False,False])
        map.drawmeridians(meridians, linewidth=0.15, labels=[False,False,False,True])
    
    # draw coastlines, country boundaries, fill continents.
    map.drawcoastlines(linewidth=0.25)
    #map.drawcountries(linewidth=0.25)
    map.fillcontinents(color='coral',lake_color='aqua')
    map.drawmapboundary(fill_color='aqua')
    
    # plot lines and points
    map.plot(la, fi, color='k', linewidth=0.15, linestyle='dashdot', latlon=True)
    
    # plot points
    map.plot(la[0], fi[0], marker='o', color='g', markersize=2, latlon=True)
    map.plot(la[-1], fi[-1], marker='o', color='r', markersize=2, latlon=True)
    if show_mid_pts:
        map.scatter(la, fi, marker='.', color='b', s=1, latlon=True)
        
    # plot vertex point
    if pv != None:
        fi_v = pv[0]
        if pv[1] < 0:
            la_v = 360 + pv[1]
        else:
            la_v = pv[1]
        map.plot(la_v, fi_v, marker='o', color='yellow', markersize=2, latlon=True)
    
    if file_name != None:
        mpl.savefig(file_name)  
    mpl.show()
    
    
# Plot loxodrome path
def plotRLPath(pts, dfi, dla, fn=None):
    
    plotPath(pts, dfi, dla, 'merc', False, fn)
    
    
# Plot orthodrome path
def plotGCPath(pts, pv, dfi, dla, fn=None):
    
    plotPath(pts, dfi, dla, 'ortho', False, fn, pv)
    
    
# Plot orthodrome-loxodrome path
def plotGCRLPath(pts, dfi, dla, fn=None):
    
    plotPath(pts, dfi, dla, 'merc', True, fn)
    
