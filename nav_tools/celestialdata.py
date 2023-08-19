# -*- coding: utf-8 -*-
"""
Created on Sat Mar 20 10:39:26 2021

@author: aleksander.grm@fpp.uni-lj.si
"""
# Native python modules
import os
import sys

# Utils
from astropy.time import Time
import astropy.utils.data as aud

# Astronomy modules
import skyfield.api as sfa
from skyfield.data import hipparcos
import skyfield.almanac as sfalm

import starobject as starobj
import planetobject as planetobj
import navigationalstars as navstars

class CelestialData:
    def __init__(self,path):
        
        self.root_path = path
        
        # skyfield loader object with specified data path
        load = sfa.Loader(self.root_path)
        
        # Online time scale object refreshed every 30 days            
        self.ts = self.get_timescale(load)
            
        # load the Hipparcos catalog as a 118,218 row Pandas dataframe.
        self.df = self.get_star_db(load)
        
        # set Navigational Stars database
        self.star_db = self.get_nav_stars_db() 
        
        # get solar objects for epoch
        # 0: [1900,2050]
        # 1: [1900,2200]
        # 2: [1900,2750]
        self.solar_db = self.get_solar_db(load,0)[0]
        self.solar_eph = self.get_solar_db(load,0)[1]
        
        # All celestial object except Earth
        # [obj_id, obj_name]
        self.celestial_objects = self.get_celestial_db()
        
        # Set solar objects
        self.solar = []
        for k in self.solar_db.keys():
            if k != 'earth':
                self.solar.append(k)

# ***********************
# *** Public methods ****
# ***********************

    # returns data of all navigational celestial objects data
    def get_all_celestial_objects_data(self, date, time, pos):
        
        data = []
        for name in self.solar_db.keys():
            if name != 'earth':
                data.append(self.get_celestial_data(name, date, time, pos))
        
        for name in self.star_db.keys():
            data.append(self.get_celestial_data(name, date, time, pos))
                        
        return data
                        
                        
    def get_celestial_objects(self):
        
        return self.celestial_objects
    
    def get_celestial_data(self, name, date, time, pos):
        
        # date = [dd,mm,YYYY]
        # time = [HH,MM,SS]
        time_flt = self.filter_list_of_int(time)
        date_flt = self.filter_list_of_int(date)
        
        t = date_flt + time_flt
        #print('filtered t:', t)
    
        cb_db = self.get_all_celestial_objects_db()
        
        if name in self.solar:
            otype = 'solar'
            data_time = self.get_planet_data(name, t)
            if pos != None:
                data_pos = self.get_planet_altaz(name, t, pos)
                
        else:
            otype = 'star'
            data_time = self.get_star_data(name, t)
            if pos != None:
                data_pos = self.get_star_altaz(name, t, pos)
        
        data = [
            ['type',otype],
            ['cbody', name],
            ['name', cb_db[name]],
            ['date', '{:d}/{:d}/{:d}'.format(t[0],t[1],t[2])],
            ['time', '{:d}:{:d}:{:d}'.format(t[3],t[4],t[5])],
            ['dec', data_time['dec']],
            ['gha', data_time['gha']],
            ['gha_a', data_time['gha_a']],
            ['sha', data_time['sha']],
            ['hp', data_time['hp']],
            ['sd', data_time['sd']],
            ]
        
        if otype == 'star':
            data.append(['dist', '{:.5f} LY'.format(data_time['dist'])])
        else:
            data.append(['dist', '{:.5f} AU'.format(data_time['dist'])])
        
        if pos != None:
            lha = data_time['gha'] + pos[1]
            if lha < 0.0:
                lha = lha + 360.0
            elif lha > 360.0:
                lha = lha - 360.0
                
            data.append(['hc', data_pos['alt']])
            data.append(['wc', data_pos['az']])
            data.append(['lha', lha])
        else:
            data.append(['hc', ""])
            data.append(['wc', ""])
            data.append(['lha', ""])
        
        return dict(data)

    # name: must be from csv file
    # time: must be in list format [yyyy,mm,dd,HH,MM,SS]
    def get_star_data(self,name,t):
        
        hip = self.star_db[name][1]
        
        if hip == None:
            return 'star name: {:} UNKNOWN !!!'.format(name)
        
        earth = self.solar_db['earth'][1]
        
        ss = starobj.StarObject(name,hip,earth,self.df)
        utc = self.ts.ut1(t[0],t[1],t[2],t[3],t[4],t[5])
        
        #print('star - t:', t)
        #print('Date-Time:', utc.utc_strftime())
        
        return ss.get_astro_data(utc)
    
    # name: name must be from csv file
    # t: time must be in list format [yyyy,mm,dd,HH,MM,SS]
    # pos: position must be in format decimal degrees [+-lat, +-long]
    def get_star_altaz(self,name,t,pos):
        
        hip = self.star_db[name][1]
        
        if hip == None:
            return 'star name: {:} UNKNOWN !!!'.format(name)
        
        earth = self.solar_db['earth'][1]
        
        ss = starobj.StarObject(name,hip,earth,self.df)
        utc = self.ts.ut1(t[0],t[1],t[2],t[3],t[4],t[5])
        
        return ss.get_altaz(utc, pos)
    
    # name: Sun, Moon, Venus, Mars, Jupyter, Saturn
    # time: must be in list format [yyyy,mm,dd,HH,MM,SS]
    def get_planet_data(self,name,t):
        
        peph = self.solar_db[name][1]
        prad = self.solar_db[name][2]
        
        if peph == None:
            return 'planet name: {:} UNKNOWN !!!'.format(name)
       
        earth = self.solar_db['earth'][1]
        
        pp = planetobj.PlanetObject(peph,prad,earth)
        utc = self.ts.ut1(t[0],t[1],t[2],t[3],t[4],t[5])

        #print('planet - t:', t)
        #print('Date-Time:', utc.utc_strftime())
        
        return pp.get_astro_data(utc)
    
    # returns Aries greenwich hour angle
    def get_aries_gha(self,t):
        
        utc = self.ts.ut1(t[0],t[1],t[2],t[3],t[4],t[5])
        gha_a = 180.0 * utc.gast / 12.0
        
        return gha_a
        

    # name: name must be from csv file
    # t: time must be in list format [yyyy,mm,dd,HH,MM,SS]
    # pos: position must be in format decimal degrees [+-lat, +-long]
    def get_planet_altaz(self,name,t,pos):
        
        peph = self.solar_db[name][1]
        prad = self.solar_db[name][2]
        
        if peph == None:
            return 'planet name: {:} UNKNOWN !!!'.format(name)
       
        earth = self.solar_db['earth'][1]
        
        pp = planetobj.PlanetObject(peph,prad,earth)
        utc = self.ts.ut1(t[0],t[1],t[2],t[3],t[4],t[5])
        
        return pp.get_altaz(utc,pos)

    # date: date must be in list format [yyyy, mmm, ddd]
    # pos: position must be in decimal degree format [fi, la]
    # returns sunrise and sunset in list of strings [sunrise,sunset] in UTC zone
    def get_sunrise_sunset(self,date,pos):

        eph = self.solar_eph
        location = sfa.wgs84.latlon(pos[0], pos[1], pos[2])
        d = self.filter_list_of_int(date)
        t0 = self.ts.utc(d[0],d[1],d[2])
        t1 = self.ts.utc(d[0],d[1],d[2]+1)
        
        t, y = sfalm.find_discrete(t0, t1, sfalm.sunrise_sunset(eph, location))

        # 0 - sun rise
        # 1 - sun set
        str_time = t.utc_strftime('%Y,%m,%d,%H,%M,%S')
        
        return [self.filter_list_of_int(str_time[0].split(',')), self.filter_list_of_int(str_time[1].split(','))]

    # date: date must be in list format [yyyy, mmm, ddd]
    # pos: position must be in decimal degree format [fi, la]
    # returns sunrise and sunset in list of strings [sunrise,sunset] in UTC zone
    def get_meridian_transit(self,date,pos):

        eph = self.solar_eph
        location = sfa.wgs84.latlon(pos[0], pos[1], pos[2])
        d = self.filter_list_of_int(date)
        t0 = self.ts.utc(d[0],d[1],d[2])
        t1 = self.ts.utc(d[0],d[1],d[2]+1)
        
        t, y = sfalm.find_discrete(t0, t1, sfalm.meridian_transits(eph, eph['Sun'], location))

        # 0 - antimeridian passage
        # 1 - meridian passage
        str_time = t.utc_strftime('%Y,%m,%d,%H,%M,%S')
        
        return self.filter_list_of_int(str_time[1].split(','))


    # date: date must be in list format [yyyy, mmm, ddd]
    # t: time must be in list format [yyyy,mm,dd,HH,MM,SS]
    # pos: position must be in format decimal degrees [+-lat, +-long]
    # Returns Sun celestial data
    def get_sun_data(self, date, time, pos):

        data = self.get_celestial_data('sun', date, time, pos)

        return data
        
# ***********************
# *** Private methods ***
# ***********************

    # Set timescale for date & time conversions
    def get_timescale(self,load):

        # Online time scale object refreshed every 30 days
        db = 'finals2000A.all'
        db_path = self.root_path + '/' + db

        
        
        if not(os.path.exists(db_path)):
            Time.now().ut1  
            aud.export_download_cache(db_path, overwrite=True)
            #load.download(db)
        elif load.days_old(db) > 30.0: # check if new is on
            Time.now().ut1  
            aud.export_download_cache(db_path, overwrite=True)
            #load.download(db) 
            
        ts = load.timescale(builtin=False) # timescale 
            
        return ts

    # Set star dataframe
    def get_star_db(self,load):
            
        # load the Hipparcos catalog as a 118,218 row Pandas dataframe.
        with load.open(hipparcos.URL) as f:
            df = hipparcos.load_dataframe(f)
        
        return df
        
    # Set celestial objects
    def get_solar_db(self,load,ephmid):
        
        # define underlying ephemeris
        ephemeris = [['de421.bsp',1900,2050],
                     ['de405.bsp',1900,2200],
                     ['de406.bsp',1900,2750]]

        #hipparcos_epoch = ts.tt(1991.25)
        if ephmid in set([0, 1, 2]):
            db = ephemeris[ephmid][0]    # load chosen ephemeris
            
        db_path = self.root_path + '/' + db
        
        if not(os.path.exists(db_path)):
            load.download(db)
            
        eph = load(db)
        
        earth   = eph['earth']
        moon    = eph['moon']
        sun     = eph['sun']
        venus   = eph['venus']
        mars    = eph['mars']
        jupiter = eph['jupiter barycenter']
        saturn  = eph['saturn barycenter']
    
        # navigational planets, sun and moon 
        solar = {
            'sun' : ['Sun', sun, 696340.0],
            'moon' : ['Moon', moon, 1737.1],
            'venus' : ['Venus', venus, 6051.8],
            'mars' : ['Mars', mars, 3389.5],
            'jupiter' : ['Jupiter', jupiter, 69911.0],
            'saturn' : ['Saturn', saturn, 58232.0],
            'earth' : ['Earth', earth, 6371.0]
            }
        
        return [solar,eph]
        
    
    # Read stars ID from Hipparcos database, to get their astronomical coordinates
    def get_nav_stars_db(self):
    
        ns_obj = navstars.NavigationalStar()
        ns_db = ns_obj.getStarDB()
        
        return ns_db
    
    def get_celestial_db(self):
        
        data = []
        
        for k in self.solar_db.keys():
            if k != 'earth':
                data.append([k,self.solar_db[k][0]])
        
        data.append(["","--------"])
                
        for k in self.star_db.keys():
                data.append([k,self.star_db[k][0]])
        
        return dict(data)
                        
    def get_all_celestial_objects_db(self):
        
        data = []
        
        for k in self.solar_db.keys():
            if k != 'earth':
                data.append([k,self.solar_db[k][0]])
                
        for k in self.star_db.keys():
                data.append([k,self.star_db[k][0]])
        
        return dict(data)

    def filter_list_of_int(self, list_data):

        ld_filtered = []
        for ld in list_data:
            if isinstance(ld, str):
                ss = ld.lstrip('0') # remove leading zeros
                ld_filtered.append(int(ss))
            elif isinstance(ld, int):
                ld_filtered.append(int(ld))
            else:
                print('  ERROR: Expected integer list, but got something strange',)
                print('     -> ', list_data)
                print()
                sys.exit()

        return ld_filtered 
                
    
                
                
        
    
    
    