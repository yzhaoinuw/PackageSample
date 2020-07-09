#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun 18 13:09:41 2020

@author: yue
"""

import os
import pkg_resources

from MFJ.shelter_detection import (
                                   scrape_shelters_directory,
                                   make_shelter_list,
                                   create_database
                                   )
#%%
def main():
    source = pkg_resources.resource_filename('MFJ',
                                             'shelter_detection/resources/')
    state_url_path = source+'state_url_source'
    shelter_csv_path = source+'shelter_by_state'
    db_path = source+'shelter_list.db'
    if os.path.isdir(state_url_path):
        k = 1
        bundled = False
        while not bundled:
            bundle_folder_path = source+'old_directory_data'+str(k)
            try:
                os.mkdir(bundle_folder_path)
                bundled = True
            except FileExistsError:
                k += 1
        os.rename(state_url_path,os.path.join(bundle_folder_path,'state_url_source/'))
        print ('bundled old shelter address data into '+bundle_folder_path)
    if os.path.isdir(shelter_csv_path):
        os.rename(shelter_csv_path,os.path.join(bundle_folder_path,'shelter_by_state/'))
        
    if os.path.exists(db_path):
        os.rename(db_path,os.path.join(bundle_folder_path,'shelter_list.db'))  
        
    #%%
    print ('scraping shelter data from "https://www.homelessshelterdirectory.org/"...')    
    scrape_shelters_directory.scrape()
    print ('done')
    
    print ('making csv files from scraped data.')
    make_shelter_list.make_csv()
    print ('done')
    
    print ('creating database and table...')
    create_database.initialize_db()
    print ('done')
    
    print ('populating table...')
    create_database.enter_data()
    print ('done')

#%%
if __name__ == "__main__":
    main()      