#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb 20 11:06:11 2020

@author: yue
"""

import os
import random
import argparse
import numpy as np
import pandas as pd
from MFJ.name_parser import validate,process_name

#%%
def assign_labels(name_part,part_type):
    ''' no longer consider noise '''
    labels = []
    types = {'last':'LAST','first':'FIRST','middle':'MIDDLE',
             'suffix':'SUFFIX','non-person':'ENTITY',
             'noise':'O',
             }
    label_type = types[part_type]
    head = lambda x: 'B-' if x == 0 else 'I-'
    #head2 = lambda x: ''
    parts = name_part.split()
    # if part_type == 'noise':
    #     head = head2
    for i in range(len(parts)):
        labels.append(head(i)+label_type)
    return {'parts':parts,'labels':labels}    

#%%
def annotate(last,first,middle,suffix):
    # each name part is a dictionary with keys 'parts' and 'labels'
    parts = []
    labels = []
    sep = {'parts':',','labels':'O'}
    # five formats of presenting a name
    form1 = [last,sep,first,middle,sep,suffix]
    form2 = [last,sep,first,middle,suffix]
    form3 = [last,suffix,sep,first,middle]
    form4 = [last,first,middle,suffix]
    form5 = [first,middle,last,suffix]
    form6 = [first]
    form7 = [last]
    form8 = [first,last]
    form9 = [last,sep,first]
    form = random.choice([form1,form2,form3,form4,form5,
                          form6,form7,form8,form8,form9])
    for item in form:
        parts.extend(item['parts'])
        labels.extend(item['labels'])
    # prevent leading comma   
    if len(parts) > 0:         
        if parts[0] == ',':
            del parts[0]
            del labels[0]
        # prevent trailing comma    
        if parts[-1] == ',':
            del parts[-1]
            del labels[-1]
    return {'parts':parts,'labels':labels}   

#%%
def get_names_dataset(names_file,frac=1):
    ''' this function will deduplicate names and store them in memory '''
    if not names_file.endswith('.csv'):
        raise TypeError('The data must be presented as a csv file.')  

    df = pd.read_csv(names_file, header=None)
    if not df.iloc[:,0].dtype == 'object':
        raise TypeError('All names must be string')   
    # limit data to 1 million rows
    names = df.iloc[:1000000,0].sample(frac=1)
    distinct_names = names.unique()
    df = pd.Series(distinct_names)
    # split into train,dev,test set by 7:2:1
    train,dev,test = np.split(df.sample(frac=1), [int(.7*len(df)), int(.9*len(df))])
    return {'train':train,'dev':dev,'test':test}

#%%
def make_person_name_dataset(names_list,write_path,dataset):
    outfile1 = open(os.path.join(write_path,dataset+'.txt'),'a')
    for name in names_list:
        if not validate(name):
            continue
        name_parts = name.split('&')
        for i,part in enumerate(name_parts):
            name_parts[i] = process_name(part)
        #print (name_parts)
        assign_last = assign_labels(name_parts[0],'last')
        assign_first = assign_labels(name_parts[1],'first')
        assign_middle = assign_labels(name_parts[2],'middle')
        assign_suffix = assign_labels(name_parts[3],'suffix')
        annotations = annotate(assign_last,assign_first,
                               assign_middle,assign_suffix)
        parts = annotations['parts']
        labels = annotations['labels']
        if len(parts) == 0:
            continue
        for i,name_part in enumerate(parts):
            outfile1.write(name_part+'\t'+labels[i]+'\n')
        outfile1.write('\n') # one empty line between annotations
    outfile1.close()    
     
def make_entity_name_dataset(names_list,write_path,dataset):
    outfile1 = open(os.path.join(write_path,dataset+'.txt'),'a')
    for name in names_list:   
        if not validate(name):
            continue
        name = process_name(name)
        annotations = assign_labels(name,'non-person')
        parts = annotations['parts']
        labels = annotations['labels']
        for i,name_part in enumerate(parts):
            outfile1.write(name_part+'\t'+labels[i]+'\n')
        outfile1.write('\n') # one empty line between annotations
    outfile1.close()       
        
#%%    
    
def main():    
    parser = argparse.ArgumentParser()
    parser.add_argument("file_path", 
                        help="path to the name file",
                        )
    parser.add_argument("write_loc", 
                        help="path to the dataset folder",
                        )
    parser.add_argument("--name_type",
                        choices=['person_name','entity_name'],
                        help="person_name or entity name",
                        nargs='?',
                        default='person_name',
                        const='person_name')
    args = parser.parse_args()
    data_file = args.file_path
    write_path = args.write_loc
    if not os.path.isdir(write_path):
        os.mkdir(write_path)
    datasets = get_names_dataset(data_file) 
    if args.name_type == 'person_name':
        make_dataset = make_person_name_dataset
    else:
        make_dataset = make_entity_name_dataset  
    for data_name,name_list in datasets.items():    
        make_dataset(name_list,write_path,data_name)

#%%
if __name__ == "__main__":
    main()
