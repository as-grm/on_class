# -*- coding: utf-8 -*-
"""
Created on Sat Mar 20 09:09:02 2021

@author: aleksander.grm@fpp.uni-lj.si
"""

import math

# Astronomy modules
import skyfield.api as sfa

class StarObject:
    def __init__(self,name,hip,earth,df):
        self.name = name   # Star name
        self.hip = hip     # Star hipparcos ID
        self.earth = earth # Earth object from ephemeris
        self.df = df       # Hipparcos data-frame   
        
        # all data are set in degrees
        self.dec = 0.0    # declination [deg]
        self.gha = 0.0    # greenwich hour angle [deg]
        self.sha = 0.0    # siderial hour angle [deg]
        self.gha_a = 0.0  # aries greenwich hour angle [deg]
        self.hp = 0.0     # horizontal paralax [deg]
        self.sd = 0.0     # aparent semi diameter angle [deg]
        self.dist = 0.0   # distance [LY]
        self.alt = 0.0    # altitude [deg]
        self.az = 0.0     # azimuth [deg]
        
        self.star_hip = sfa.Star.from_dataframe(self.df.loc[int(self.hip)])

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
        
        self.set_altaz(t, pos)
        
        data = {
            'alt' : self.alt,
            'az' : self.az,
            }
        
        return data
    
   
# ***************************    
# **** Private functions ****
# ***************************

    # Sets astro data: declination, sha, gha_aries and dist for time t
    # time t must be in the skyfield timescale format
    # formaly it is UTC time - tc.utc()
    def set_astro_data(self,t):
        
        # apparent() corrects for:
        # Deflection: light passing near massive objects
        # Aberration: Earth moves fast (like rain in a car) 
        astrometric = self.earth.at(t).observe(self.star_hip).apparent()
        ra, dec, dist = astrometric.radec(epoch='date')
        
        self.dec = dec.degrees
        self.sha = self.gha2deg(0,ra.hours)
        self.gha_a = 180. * t.gast / 12.
        
        self.gha = self.gha_a + self.sha
        if self.gha > 360.0:
            self.gha = self.gha - 360.0
        
        # Calculate distanc in light Years
        ys = 60*60*24*365
        self.dist = (dist.km / 299792.458)/ys
        
        self.hp = math.atan(6371.0 / dist.km) * 180.0/math.pi
    
    # Sets star altitude and azimuth
    # pos: latitude, longitude in degrees
    def set_altaz(self,t,pos):
        
        location = self.earth + sfa.wgs84.latlon(pos[0], pos[1], pos[2])
        # apparent() corrects for:
        # Deflection: light passing near massive objects
        # Aberration: Earth moves fast (like rain in a car) 
        astrometric = location.at(t).observe(self.star_hip).apparent()
        # altaz(temperature_C=None, pressure_mbar='standard')
        # Correction for refraction: enter data for temperature/pressure
        alt, az, d = astrometric.altaz()
        
        self.alt = alt.degrees
        self.az = az.degrees
        
    # convert GHA (hours) to degrees of arc
    def gha2deg(self,gst, ra):
    
        sha = (gst - ra) * 15
        while sha < 0:
            sha = sha + 360
        
        return sha

