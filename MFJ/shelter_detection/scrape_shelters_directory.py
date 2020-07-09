#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr  3 14:51:59 2020

@author: yuezhao
"""

import os
import requests
import pkg_resources

from bs4 import BeautifulSoup

def scrape(resources_path=None):
    s = requests.session()
    home_url = 'https://www.homelessshelterdirectory.org/'
    r = requests.get(home_url)
    soup = BeautifulSoup(r.text,'lxml')
    #%%
    state_list = soup.find('select',id='states_home_search')
    states = state_list.find_all('option')
    state_url = {}
    for state in states:
        if state['value'].endswith('html'):
            state_name = state['value'].split('.html')[0]
            state_url[state_name] = home_url+state['value']
    #%%   
    # the following three states are misspelled in the url        
    del state_url['lousiiana'] 
    state_url['louisiana'] = 'https://www.homelessshelterdirectory.org/louisiana.html'
    
    del state_url['misssissippi'] 
    state_url['mississippi'] = 'https://www.homelessshelterdirectory.org/mississippi.html'
    
    del state_url['misouri'] 
    state_url['missouri'] = 'https://www.homelessshelterdirectory.org/missouri.html'    
    #%% 
    city_url = {} 
    for state in state_url:       
        r2 = requests.get(state_url[state]) 
        soup2 = BeautifulSoup(r2.text,'lxml') 
        try:     
            city_list = soup2.find('ul',id='triple').find_all('a')
        except AttributeError:
            print (state)
        for city in city_list:
            city_name = city.get_text()+', '+state
            city_url[city_name] = city['href']
    
    #%%
    #shelter_url = []
    if resources_path is None:
        resources_path = pkg_resources.resource_filename('MFJ',
                                                         'shelter_detection/resources/state_url_source/')
    if not os.path.isdir(resources_path):
        os.mkdir(resources_path)
    prev_state = ''    
    for city in city_url: 
        state = city.split(', ')[1]    
        if state != prev_state:
            print ('scraping the state of '+state)
        prev_state = state    
        outfile = open(resources_path+state+'.txt', 'a')
        r3 = requests.get(city_url[city]) 
        soup3 = BeautifulSoup(r3.text,'lxml') 
        shelter_list = soup3.find('div',{"class": "listings"}) 
        shelters = shelter_list.find_all('div',{"class": "item_content"})
        for shelter in shelters:
            entry = shelter.find('h4').find('a')
            shelter_name = entry.get_text()
            try:
                url = entry['href']
                outfile.write(city+', '+shelter_name+', '+url+'\n')
                #shelter_url.append([city,shelter_name,url])
            except KeyError:
                print ('no url found for ',shelter_name, ' in', city)
                outfile.write(city+', '+shelter_name+'\n')
        outfile.close()        
#%%        
if __name__ == '__main__':
    scrape()