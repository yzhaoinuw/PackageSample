#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May 19 17:39:13 2020

@author: yue
"""


import os
import pkg_resources

import sqlite3
import usaddress
import pandas as pd
from usaddress import RepeatedLabelError

#from normalize_address import normalize
from MFJ.shelter_detection.normalize_address import normalize
#%%
def initialize_db(db_loc=None):
    if db_loc is None:
        db_loc = pkg_resources.resource_filename('MFJ',
                                                 'shelter_detection/resources/shelter_list.db')
    conn = sqlite3.connect(db_loc)
    cur = conn.cursor()
    # Create table
    cur.execute('''CREATE TABLE IF NOT EXISTS shelters (
                 ID CHAR (20) PRIMARY KEY, 
                 ShelterName NOT NULL, 
                 Phone,
                 Website,             
                 AddressType CHAR (15) NOT NULL ,
                 StreetAddress NOT NULL,
                 USPSBoxType,
                 USPSBoxID,
                 USPSBoxGroupType,
                 USPSBoxGroupID,              
                 PlaceName, 
                 StateName, 
                 StateCode CHAR (2), 
                 ZipCode, 
                 UNIQUE(ShelterName,
                 StreetAddress) ON CONFLICT IGNORE
                 );''')

#%%
def enter_data(db_loc=None,data_source=None):
    if db_loc is None:
        db_loc = pkg_resources.resource_filename('MFJ',
                                                 'shelter_detection/resources/shelter_list.db')        
    if data_source is None:
        data_source = pkg_resources.resource_filename('MFJ',
                                                      'shelter_detection/resources/shelter_by_state/')
    folder = os.listdir(data_source) 
    problematic_address = set([])
    non_standardizable = set([])
    other_address = set([])
    for file in folder:
        if file.endswith('.csv'):
            conn = sqlite3.connect(db_loc)
            cur = conn.cursor()
            state = file.split('.csv')[0] 
            df = pd.read_csv(data_source+file,header=0) 
            for index, row in df.iterrows():
                ShelterName = row['shelter name']
                if pd.isnull(ShelterName):
                    continue
                ID = state+'_'+str(index)
                ShelterName = ShelterName.strip().upper()
                Address = row['address'].strip().upper()
                StreetAddress = ''
                Phone = str(row['phone']).strip()
                Website = str(row['website']).strip()    
                AddressType = 'Problematic'
                PlaceName = ''
                StateCode = ''
                StateName = row['state'].strip().upper()
                ZipCode = ''
                USPSBoxType = ''
                USPSBoxID = ''
                USPSBoxGroupType = ''
                USPSBoxGroupID = ''             
                
                try:
                    address_parts = usaddress.tag(Address)
                    AddressType = address_parts[1]
                    tags = address_parts[0]
                    street_parts = []
                    if 'PlaceName' in tags:
                        PlaceName = tags['PlaceName']
                        del tags['PlaceName']
                    if 'StateName' in tags:
                        StateName = tags['StateName']
                        del tags['StateName']  
                    if 'ZipCode' in tags:
                        ZipCode = tags['ZipCode']
                        del tags['ZipCode']                     
                    for tag,value in tags.items():
                        street_parts.append(value)
                        StreetAddress = ' '.join(street_parts)
                    # only normalize a legit street address
                    if AddressType == 'Street Address':
                        standardized = normalize(StreetAddress)
                        if standardized is not False:
                            StreetAddress = standardized
                        else:    
                            non_standardizable.add(StreetAddress)
                    elif AddressType == 'PO Box':
                        if 'USPSBoxType' in tags:
                            USPSBoxType = tags['USPSBoxType']
                        if 'USPSBoxID' in tags:
                            USPSBoxID = tags['USPSBoxID']
                        if 'USPSBoxGroupType' in tags:
                            USPSBoxGroupType = tags['USPSBoxGroupType']
                        if 'USPSBoxGroupID' in tags:
                            USPSBoxGroupID = tags['USPSBoxGroupID']                   
                    else:    
                        other_address.add(StreetAddress)
                             
                except RepeatedLabelError:
                    problematic_address.add(Address)
                    StreetAddress = Address
    
                transaction = (ID,ShelterName,Phone,Website,AddressType,StreetAddress,
                               USPSBoxType,USPSBoxID,USPSBoxGroupType,USPSBoxGroupID,
                               PlaceName,StateName,StateCode,ZipCode,)
    
                cur.execute("INSERT INTO shelters VALUES" +"("+"?,"*13+"?)", transaction)    
            conn.commit()
            conn.close() 
                
#%%
if __name__ == '__main__':
    initialize_db()
    enter_data()