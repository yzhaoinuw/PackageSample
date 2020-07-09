#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May 22 09:16:57 2020

@author: yue
"""


#%%
import pandas as pd
from MFJ.shelter_detection import query_address

data_file = 'path_to/wi_extract_addr.csv'
fields = ['DefCity','DefState','DefZip','DefPrimaryAddress']
df = pd.read_csv(data_file,header=0,usecols=fields).dropna()
#%%
import time

start_time = time.time()

db = query_address.ConnectDB()
match = []
for index, row in df.iterrows():
    
    address = {'StateName':row['DefState'],'ZipCode':str(row['DefZip']),
               'PlaceName':row['DefCity'],'StreetAddress':row['DefPrimaryAddress']}
    #state_zip = ' '.join([row['DefState'],str(row['DefZip'])])
    #address = ', '.join([row['DefPrimaryAddress'],row['DefCity'],state_zip])
    result = db.is_shelter(address)
    if result:
        match.append(address)

        
runtime = time.time() - start_time 
    
#%%
print (runtime)
print (index)
print (match)

