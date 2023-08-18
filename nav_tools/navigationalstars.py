#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Feb 20 10:48:33 2022

@author: sandro
"""

import sys

class NavigationalStar:
    def __init__(self):
        self.star_DB = self.fillStarDB() # Navigational stars database

# **********************
# *** Public methods ***
# **********************
    
    # returns navigational stars database
    def getStarDB(self):
        
        return self.star_DB
    
    
    # returns star long name 
    def getStarName(self,star_id):
        
        try:
            star = self.star_DB[star_id]
        except ValueError:
            print("  **ERROR**: Star ID '{:s}' is not in the list of navigational stars!".format(star_id))
            sys.exit()
        
        return star[0]
    
    
    # returns star HIP 
    def getStarHIP(self,star_id):
        
        try:
            star = self.star_DB[star_id]
        except ValueError:
            print("  **ERROR**: Star ID '{:s}' is not in the list of navigational stars!".format(star_id))
            sys.exit()
        
        return star[1]
    
   
# ***************************    
# **** Private functions ****
# ***************************

    def getIDs(self):
        
        star_id = ['acamar','achernar','acrux','adhara','aldebaran','alioth',
                   'alkaid','al_nair','alnilam','alphard','alphecca','alpheratz',
                   'altair','ankaa','antares','arcturus','atria','avior',
                   'bellatrix','betelgeuse','canopus','capella','deneb','denebola',
                   'diphda','dubhe','elnath','eltanin','enif','fomalhaut','gacrux',
                   'gienah','hadar','hamal','kaus_au','kochab','markab','menkar',
                   'menkent','miaplacidus','mirfak','nunki','peacock','polaris',
                   'pollux','procyon','rasalhague','regulus','rigel','rigil_kent',
                   'sabik','scheat','schedar','shaula','sirius','spica','suhail',
                   'vega','zubenelgenubi']
        
        return star_id
    
    def getNames(self):
        
        star_name = ['Acamar','Achernar','Acrux','Adhara','Aldebaran','Alioth',
                     'Alkaid','Al Na’ir','Alnilam','Alphard','Alphecca','Alpheratz',
                     'Altair','Ankaa','Antares','Arcturus','Atria','Avior',
                     'Bellatrix','Betelgeuse','Canopus','Capella','Deneb','Denebola',
                     'Diphda','Dubhe','Elnath','Eltanin','Enif','Fomalhaut','Gacrux',
                     'Gienah','Hadar','Hamal','Kaus Australis','Kochab','Markab',
                     'Menkar','Menkent','Miaplacidus','Mirfak','Nunki','Peacock',
                     'Polaris','Pollux','Procyon','Rasalhague','Regulus','Rigel',
                     'Rigil Kentaurus','Sabik','Scheat','Schedar','Shaula','Sirius',
                     'Spica','Suhail','Vega','Zuben El Genubi']
        
        return star_name
    
    def getHIPs(self):
        
        star_HIP = [13847,7588,60718,33579,21421,62956,67301,109268,26311,46390,
                    76267,677,97649,2081,80763,69673,82273,41037,25336,27989,30438,
                    24608,102098,57632,3419,54061,25428,87833,107315,113368,61084,
                    59803,68702,9884,90185,72607,113963,14135,68933,45238,15863,
                    92855,100751,11767,37826,37279,86032,49669,24436,71683,84012,
                    113881,3179,85927,32349,65474,44816,91262,72622]
        
        return star_HIP
    
    
    # returns navigational stars database
    def fillStarDB(self):
        
        s_id = self.getIDs()
        s_name = self.getNames()
        s_hip = self.getHIPs()
        
        data = []
        nn = len(s_id)
        for i in range(nn):
            data.append([s_id[i],[s_name[i],int(s_hip[i])]])
        
        return dict(data)
        
        
        
        
        
        