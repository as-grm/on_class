# -*- coding: utf-8 -*-
"""
Created on Sat Mar 20 09:09:02 2021

@author: aleksander.grm@fpp.uni-lj.si
"""

import math

# Astronomy modules
import skyfield.api as sfa


class PlanetObject:
    def __init__(self,eph,radius,earth):
        
        self.eph = eph       # solar object eph object
        self.radius = radius # solar object radius
        self.earth = earth   # Earth object from ephemeris
        
        # all astronomical data for time t
        self.dec = 0.0    # declination [deg]
        self.gha = 0.0    # greenwich hour angle [deg]
        self.sha = 0.0    # siderial hour angle [deg]
        self.gha_a = 0.0  # aries greenwich hour angle [deg]
        self.hp = 0.0     # horizontal paralax [deg]
        self.sd = 0.0     # aparent semi diameter angle [deg]
        self.dist = 0.0   # distance [km]
        self.alt = 0.0    # altitude [deg]
        self.az = 0.0     # azimuth [deg]

# **********************
# *** Public methods ***
# **********************

    # returns astro data for time t in dictionary object 
    # time t must be in the skyfield timescale format
    # formaly it is UTC time - tc.utc()
    # internaly handeled in UT1
    def get_astro_data(self,t):
        
        self.set_astro_data(t)
        
        data = {
            'dec' : self.dec,
            'gha' : self.gha,
            'sha' : self.sha,
            'gha_a' : self.gha_a,
            'hp' : self.hp,
            'sd' : self.sd,
            'dist' : self.dist
            }
        
        return data
    
    # returns altitude and azimuth for time t in dictionary object 
    # time t must be in the skyfield timescale format
    # formaly it is UTC time - tc.utc()
    # internaly handeled in UT1
    def get_altaz(self,t,pos):
        
        self.set_altaz(t,pos)
        
        data = {
            'alt' : self.alt,
            'az' : self.az,
            }
        
        return data
   
# ***************************    
# **** Private functions ****
# ***************************

    # Sets all astro data for time t
    # time t must be in the skyfield timescale format
    # formaly it is UTC time - tc.utc()
    def set_astro_data(self,t):
        
        astrometric = self.earth.at(t).observe(self.eph).apparent()
        ra, dec, dist = astrometric.radec(epoch='date')
        
        self.dec = dec.degrees
        self.sha = self.gha2deg(0,ra.hours)
        self.gha_a = 180. * t.gast / 12.
        
        self.gha = self.gha_a + self.sha
        if self.gha > 360.0:
            self.gha = self.gha - 360.0
        
        self.dist = dist.km / 149597870.7
        
        self.hp = math.atan(6371.0 / dist.km) * 180/math.pi
        self.sd = math.atan(self.radius / dist.km) * 180.0/math.pi
        
    # Sets planet altitude and azimuth
    # pos: latitude, longitude in degrees
    def set_altaz(self,t,pos):
        
        location = self.earth + sfa.wgs84.latlon(pos[0], pos[1], pos[2])
        astrometric = location.at(t).observe(self.eph).apparent()
        alt, az, d = astrometric.altaz()
        
        self.alt = alt.degrees
        self.az = az.degrees
    
    # convert GHA (hours) to degrees of arc
    def gha2deg(self,gst, ra):
    
        sha = (gst - ra) * 15
        while sha < 0:
            sha = sha + 360
        
        return sha

