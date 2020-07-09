#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jun 21 02:27:17 2020

@author: yue
"""

from scourgify import normalize_address_record
from scourgify.exceptions import (
    AddressNormalizationError,
    AmbiguousAddressError,
    UnParseableAddressError
    )
#%%

def normalize(address):
    try:
        address = normalize_address_record(address)
    except (AddressNormalizationError,AmbiguousAddressError,
            UnParseableAddressError):
        return False
    for field,item in address.items():
        if item == None:
            address[field] = ''
    street_part = ' '.join(filter(None,[address['address_line_1'],address['address_line_2']]))
    state_part = ' '.join(filter(None,[address['state'],address['postal_code']]))   
    normalized_address =  ', '.join(filter(None,[street_part,address['city'],state_part])) 
      
    return (normalized_address)