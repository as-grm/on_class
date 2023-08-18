# -*- coding: utf-8 -*-
"""
Created on Sat Mar 20 10:39:26 2021

@author: aleksander.grm@fpp.uni-lj.si
"""

from astropy.time import Time
from astropy.utils.data import clear_download_cache

clear_download_cache()  

t = Time('2022:001')
t.ut1  
