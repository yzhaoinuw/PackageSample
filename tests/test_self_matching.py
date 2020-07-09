#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr  8 16:46:15 2020

@author: yuezhao
"""

import os
import pandas as pd
import pkg_resources
from MFJ.shelter_detection import query_address
import time

start_time = time.time()
db = query_address.ConnectDB()

#%%
match = 0
path = 'MFJ/shelter_detection/resources/shelter_by_state/'
data_path = pkg_resources.resource_filename('MFJ', path)
data_path = '../resource/shelter_by_state/'
fields = ['shelter name','address']
total_count = 0
non_match = []
folder = os.listdir(data_path)
for file in folder:
    if not file.endswith('.csv'):
        continue
    print (file)
    df = pd.read_csv(data_path+file,header=0,usecols=fields).dropna()
    for index, row in df.iterrows():
        if row['shelter name'].strip() == '':
            continue
        address = row['address']
        result = db.is_shelter(address)
        if result:
            match += 1
        else:
            non_match.append(address)
        total_count += 1  

runtime = time.time() - start_time 

#%%
  
print ("--- %s addresses per seconds ---" % str(total_count/runtime))
#%%
#print (match,total_count)
print (len(set(non_match)))

'''
address_list = ['Hwy 59 South  75901, Lufkin, TX 75901',
                '653 S. 4th Ave, Pocatello, ID 83201',
                '173 Boulevard NE, Atlanta, GA 30312',
                'Address Confidential, Ames, IA 50010',
                '641 N. 8th Ave, Pocatello, ID 83201',
                '122nd Avenue, Allegan, MI  4901',
                'confidential not provided, Mesa, AZ 85201',
                '308 S. 24th St., Boise, ID 83702',
                'address not disclosed, Cataumet, MA',
                '100 & 102 Plymouth Ave, Bakersfield, CA 93308',
                'N., 35 Public Square, Salem, IN 47167',
                'Pine Bluffs, WY',
                '840 Park Avenue, Idaho Falls, ID 83402',
                'CONFIDENTIAL, Ruston, LA 71270',
                'not provided, Turlock, CA 95353',
                '108 E. Walnut, Coeur d Alene, ID 83814',
                'Fort Lupton CO, Fort Lupton, CO 80621',
                'Elm Street, Keene, NH',
                'Confidential, Monroe, LA',
                'not provided, Sauk Village, IL 60411',
                '594 Washington St. S., Twin Falls, ID 83301',
                'CONFIDENTIAL, Hammond, LA',
                '304 16th Ave. North, Nampa, ID',
                'confidential, Atlanta, GA 30314',
                '4306 W State, Boise, ID 83703',
                'San Diego, CA 92108',
                '2480 S. Yellowstone, Idaho Falls, ID 83405',
                'not disclosed., Gainesville, FL 32601',
                'not disclosed, Cape Girardeau, MO 63701',
                '10-12 wait street, Glen Falls, NY 12801',
                '255 E Street, Idaho Falls, ID 83402',
                'Main Street, Franconia, NH 03580',
                'undisclosed location, Salinas, CA 93906',
                'PO Box 131, Planetarium Station, New York, NY 10024',
                'Scattered Sites, Newport News, VA 23601',
                "PO Box 3665, Coeur d'Alene, ID 83816",
                '1404 W. Jefferson, Boise, ID 83702',
                'Various locations all winter, Traverse City, MI 49684',
                'undisclosed location, Richmond, TX 77406',
                'Baltimore, Baltimore, MD 21229']
'''
