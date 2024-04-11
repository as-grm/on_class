#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Feb 18 12:57:30 2022

@author: sandro@fpp.uni-lj.si

File containing Navigation programming tools!
"""
from collections import Counter
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
u_delta = '\u03C9'


# Pretty print of degrees minutes form
def prettyPrintDM(x,z):
    
    x = mat.fabs(x)
    x_d = mat.floor(x)
    x_m = (x - x_d)*60.0
    
    if mat.fabs(60.0 - x_m) < 1e-3:
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


# Converts angle specified in:
#  -> [deg, min.dec]
#  -> [deg, min, sec.dec]
#  in decimal degrees
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


# Calculates delta LONG in a correct way
# All calculations are oriented eastward 0...360, opposite as the hour angle!
def deltaLong(la_0, la_1):

    if la_0 < 0:
        la0 = 360 + la_0
    else:
        la0 = la_0
    
    if la_1 < 0:
        la1 = 360 + la_1
    else:
        la1 = la_1
    
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


# Find integer start lambda based on delta lambda
def getStartLambda(la0, dl, dla):

    set = [5,10,15,20]
    count = Counter(set)
    #print('set {} has {} occurrences of {}'.format(set,count[dla],dla))
    
    if dl > 0:
        if la0 < 0:
            la_s = mat.ceil(la0)
            if count[dla] > 0:
                dla_s = mat.fmod(la_s, dla)
                la_s = la_s - dla_s
        else:
            la_s = mat.floor(la0)
            if count[dla] > 0:
                dla_s = mat.fmod(la_s, dla)
                la_s = la_s + (dla - dla_s)
    else:
        if la0 < 0:
            la_s = mat.floor(la0)
            if count[dla] > 0:
                dla_s = mat.fmod(la_s, dla)
                la_s = la_s - (dla + dla_s)
        else:
            la_s = mat.ceil(la0)
            if count[dla] > 0:
                dla_s = mat.fmod(la_s, dla)
                la_s = la_s -  dla_s
        
    return la_s


# Find midpoints in longitude range
def getMidpoints(la_0, la_1, dla):

    dl = deltaLong(la_0, la_1)
    dls = np.sign(dl)
    la_s = getStartLambda(la_0, dl, dla)
    
    mpa = []
    mpa.append(la_s)
    la = la_s

    # Map lambda into the interval [0...360], easier calculations
    if la_0 < 0:
        la0 = 360 + la_0
    else:
        la0 = la_0

    if la_1 < 0:
        la1 = 360 + la_1
    else:
        la1 = la_1

    if la_s < 0:
        las = 360 + la_s
    else:
        las = la_s

    nlp = int(np.fabs(dl/dla))
    
    la_end = las + nlp*dla*dls
    if la_end < 0:
        la_end = 360 + la_end
    if la_end > 360:
        la_end = la_end - 360

    if dls > 0:
        if la_end > la1:
            nlp = nlp - 1
    else:
        if la_end < la1:
            nlp = nlp - 1

    for i in range(nlp):
        la = la_s + (i+1)*dla*dls
        mpa.append(la)

    #print('mpa:', mpa)
    
    new_mpa = []
    for x in mpa:
        if x > 180: 
            nx = x - 360; 
        elif x < -180: 
            nx = 360 + x
        else:
            nx = x
            
        new_mpa.append(nx)

    #print('new_mpa:', new_mpa)
    
    return new_mpa    

# Find midpoints in longitude range
def getPathPointsLong(la_0, la_1, dla):
    
    mps = getMidpoints(la_0, la_1, dla)
    
    la_all = [la_0] + mps + [la_1]
    
    return la_all 
        
    
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


# Find lower left and upper right map corner
def get_corners(fi, la, dfi, dla):

    la_0 = la[0]
    la_1 = la[-1]
    dl = deltaLong(la_0,la_1)
    if la_0 < 0:
        la_0 = 360 + la[0]
    if la_1 < 0:
        la_1 = 360 + la_1
        
    fi_min = np.floor(np.min(fi))
    fi_min = fi_min - (fi_min%dfi)
    fi_max = np.ceil(np.max(fi))
    fi_max = fi_max + (dfi - fi_max%dfi)

    if dl < 0:
        la_min = la_1
        la_max = la_0
    else:
        la_min = la_0
        la_max = la_1
        
    la_min = np.floor(la_min)
    la_min = la_min - (la_min%dla)
    if la_min < 0:
        la_min = 360 + la_min
    
    
    la_max = np.ceil(la_max)
    la_max = la_max + (dla - la_max%dla)
    if la_max > 360:
        la_max = la_max - 360
    
        
    fi_mid = (fi_min + fi_max)/2
    la_mid = la_0 + dl/2

    if (la_min > la_max) and (la_min > 180):
        la_min = la_min - 360

    if la_max > 180:
        long360 = True
    else:
        long360 = False
    
        
    #print('la_min:', la_min)
    #print('la_max:', la_max)
    
    llc = [fi_min,la_min]
    urc = [fi_max,la_max]
    mp = [fi_mid,la_mid]
    #print('mp:', mp)

    return [llc, urc, mp, long360]
        

# Plot Mercator chart and path
def plotPath(pts, dfi=5, dla=10, projection='merc', show_mid_pts=False, file_name=None, pv=None):

    nn = len(pts)
    if nn < 2:
        print('Input size mismatch: len(pts)={:d}'.format(len(pts)))
        raise AssertionError()

    fi = np.transpose(pts)[0]
    la = np.transpose(pts)[1]

    #print('la:', la)
    [llc, urc, mp, long360] = get_corners(fi, la, dfi, dla)

    if long360:
        la_p = []
        for l in la:
            if l < 0:
                la_p.append(360+l)
            else:
                la_p.append(l)
    else:
        la_p = la
    #print('la_p:', la_p)
    
    fi_0 = fi[0]
    la_0 = la_p[0]
    fi_1 = fi[-1]
    la_1 = la_p[-1]
    
    fi_min = llc[0]
    fi_max = urc[0]
    la_min = llc[1]
    la_max = urc[1]
    
    #print('fi_min:', fi_min, 'fi_max:', fi_max)
    #print('la_min:', la_min, 'la_max:', la_max)
        
    fi_mid = mp[0]
    la_mid = mp[1]

    llcrnrlat_c = fi_min - 5, # lower left corner
    urcrnrlat_c = fi_max + 5,  # upper right corner
    llcrnrlon_c = la_min - 1
    urcrnrlon_c = la_max + 1
    
    #print('BB: ({:},{:}) - ({:},{:})'.format(fi_min,la_min,fi_max,la_max))
    
    if projection == 'ortho':
        map = bmap.Basemap(projection='ortho',
            lat_0 = fi_mid,
            lon_0 = la_mid,
            resolution='l') #c croud par defaut, l low , h high , f full
        
    else:
        map = bmap.Basemap(projection='merc',
            lat_ts = fi_mid,
            llcrnrlat = llcrnrlat_c, # lower left corner
            llcrnrlon = llcrnrlon_c,
            urcrnrlat = urcrnrlat_c,  # upper right corner
            urcrnrlon = urcrnrlon_c,
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
    x,y = map(la_p,fi)
    map.plot(x, y, color='k', linewidth=0.15, linestyle='dashdot', latlon=False)
    
    # plot points
    if show_mid_pts:
        map.scatter(x, y, marker='.', color='b', s=1, latlon=False)

    x0,y0 = map(la_0,fi_0)
    map.plot(x0,y0, marker='o', color='g', markersize=3, latlon=False)
    x1,y1 = map(la_1,fi_1)
    map.plot(x1,y1, marker='o', color='r', markersize=3, latlon=False)
    
        
    # plot vertex point
    if pv != None:
        fi_v = pv[0]
        if pv[1] < 0 and long360:
            la_v = 360 + pv[1]
        else:
            la_v = pv[1]
        xv,yv = map(la_v,fi_v)
        map.plot(xv,yv, marker='o', color='yellow', markersize=2, latlon=False)
    
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
    
