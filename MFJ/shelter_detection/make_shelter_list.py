#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr  3 20:49:43 2020

@author: yuezhao
"""

import os
import re
import csv
import requests
import functools
import pkg_resources
from multiprocessing import Pool

from bs4 import BeautifulSoup
#%%
def get_contact(url):
    s = requests.session()
    r = requests.get(url)
    soup = BeautifulSoup(r.text,'lxml')
    contact = soup.find('p')
    lines = contact.get_text().split('\n')
    address = []
    website = ''
    phone = ''
    for line in lines:
        line = line.strip()
        if len(line) == 0:
            continue
        if ':' not in line:
            address.append(line)
        elif 'http' in line:
           website = line.strip(': ') 
        else:
            phone_pattern = '(\d{3}[-\.\s]??\d{3}[-\.\s]??\d{4}|\(\d{3}\)\s*\d{3}[-\.\s]??\d{4}|\d{3}[-\.\s]??\d{4})'
            phone = re.search(phone_pattern,line)
            if phone != None:
                phone = phone.group()
            
    address = ', '.join(address)
    #postal_code = str(address.split()[-1])
    return {'address':address, 'website': website,
            'phone': phone}
   

def write_state(state_file,write_loc):   
    print (state_file)
    state = state_file.split('/')[-1].split('.txt')[0]
    with open(write_loc+state+'.csv', 'w') as outcsv:
        writer = csv.writer(outcsv,delimiter =',')
        writer.writerow(['shelter name', 'city', 'state',
                               'address', 'website', 'phone'])
    with open(state_file,'r') as infile:
        lines = infile.read().rstrip().split('\n')
    outcsv = open(write_loc+state+'.csv','a')  
    for line in lines:
        line = line.strip().split(', ') 
        try:
            city = line[0]
            shelter_name = line[2:-1][0]
            url = line[-1]
        except IndexError:
            pass
        contact_info = get_contact(url)
        writer = csv.writer(outcsv,delimiter =',')
        writer.writerow([shelter_name, city, state,
                       contact_info['address'], contact_info['website'], 
                       contact_info['phone']])
    outcsv.close()    

def make_csv(source=None,write_loc=None):
    if source is None:
        source = pkg_resources.resource_filename('MFJ',
                                                 'shelter_detection/resources/state_url_source/')
    if write_loc is None:
        write_loc = pkg_resources.resource_filename('MFJ',
                                                         'shelter_detection/resources/shelter_by_state/')
    if not os.path.isdir(write_loc):
        os.mkdir(write_loc)          
    folder = os.listdir(source)
    file_list = [source+file for file in folder if file.endswith('.txt')]
    pool = Pool()
    pool.map(functools.partial(write_state,write_loc=write_loc),file_list)
    '''
    for file in folder:
        if file.endswith('.txt'):
            #state = file.split('_')[-1].split('.txt')[0]          
            state_file = source+file
            write_state(state_file,write_loc)
    '''
#%%
if __name__ == '__main__':
    make_csv()            
