#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May 21 21:32:43 2020

@author: yue
"""


import sqlite3
import pkg_resources
import usaddress
from usaddress import RepeatedLabelError
#from .parse_address import parse_address
from scourgify import normalize_address_record
from scourgify import normalize
from scourgify.exceptions import (
    AddressNormalizationError,
    AmbiguousAddressError,
    UnParseableAddressError
    )

path = 'shelter_detection/resources/shelter_list.db'
db_path = pkg_resources.resource_filename('MFJ', path)

#%%
def standardize_address(address):
    try:
        address = normalize_address_record(address)
    except (AddressNormalizationError,AmbiguousAddressError,
            UnParseableAddressError):
        return False
    for field,item in address.items():
        if item is None:
            address[field] = ''
    street_part = ' '.join(filter(None,[address['address_line_1'],address['address_line_2']]))
    state_part = ' '.join(filter(None,[address['state'],address['postal_code']]))   
    normalized_address =  ', '.join(filter(None,[street_part,address['city'],state_part])) 
      
    return (normalized_address)

def standardize_state(state):
    return normalize.normalize_state(state) 

#%%
def parse_address(Address): 
    determinant = 0
    tags = None
    parsed_address = {'AddressType':'Problematic','StreetAddress':None,
                     'PlaceName':None,'StateName':None,'ZipCode':None,
                     'USPSBoxType':None,'USPSBoxID':None,'USPSBoxGroupType':None,
                     'USPSBoxGroupID': None,'valid':False}
    
    if isinstance(Address,str):
        address_line = Address.strip().upper()
    elif isinstance(Address,dict):
        tags = Address   
        address_line = str(Address['StreetAddress']).strip().upper()
    else:
        raise TypeError("Address must be a string or a dictionary.")
    
    try:
        address_parts = usaddress.tag(address_line)
    except RepeatedLabelError:
        parsed_address['valid'] = True
        parsed_address['StreetAddress'] = address_line  
        return (parsed_address)    
     
    parsed_address['AddressType'] = address_parts[1]
    if tags is None:
        tags = address_parts[0]          
                   
    if 'PlaceName' in tags:
        parsed_address['PlaceName'] = tags['PlaceName'].upper()
        determinant += 1
        del tags['PlaceName']
    if 'StateName' in tags:
        parsed_address['StateName'] = standardize_state(tags['StateName'])
        determinant += 1
        del tags['StateName']  
    if 'ZipCode' in tags:
        parsed_address['ZipCode'] = tags['ZipCode']
        determinant += 2
        del tags['ZipCode']                     
    parsed_address['StreetAddress'] = ' '.join(tags.values()).upper() 

    if len(parsed_address['StreetAddress']) == 0:
        pass
    # only standardize a legit street address
    elif parsed_address['AddressType'] == 'Street Address':
        determinant += 3
        standardized = standardize_address(parsed_address['StreetAddress'])
        if standardized is not False:
            parsed_address['StreetAddress'] = standardized
    
    elif parsed_address['AddressType'] == 'PO Box':
        if 'USPSBoxType' in tags:
            determinant += 1
            parsed_address['USPSBoxType'] = tags['USPSBoxType']
        if 'USPSBoxID' in tags:
            determinant += 2
            parsed_address['USPSBoxID'] = tags['USPSBoxID']
        if 'USPSBoxGroupType' in tags:
            determinant += 1
            parsed_address['USPSBoxGroupType'] = tags['USPSBoxGroupType']
        if 'USPSBoxGroupID' in tags:
            determinant += 2 
            parsed_address['USPSBoxGroupID'] = tags['USPSBoxGroupID']  

    if determinant >= 5:
        parsed_address['valid'] = True
    return parsed_address


#%%
class ConnectDB():
    def __init__(self):
        self.conn = sqlite3.connect(db_path)
        self.cur = self.conn.cursor()
        
    def query(self,address):
        query = []
        parse_results = parse_address(address)
        if parse_results['valid']:
            del parse_results['valid']
            for field,value in parse_results.items():
                if value is not None:
                    #make sure the value does not contain '"'
                    value = value.translate(str.maketrans('', '', '"'))
                    query.append(field+'='+'"'+value+'"')
        if len(query) > 0:   
            query = ' AND '.join(query)      
            self.cur.execute("SELECT * FROM shelters WHERE "+query)           
            rows = self.cur.fetchall() 
        else:
            rows = []
        return rows
    
    def is_shelter(self,address):
        results = self.query(address)
        if len(results) > 0:
            return True
        else:
            return False

