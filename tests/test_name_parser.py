#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat May 23 18:26:21 2020

@author: yue
"""

from MFJ.name_parser import NameParser

model_name = 'name_parser_flair_2.0_cpu'
model_name = 'name_parser_elmo_noncrf'
parser = NameParser(model_name)


#%%
import time

start_time = time.time()
name_list = []
result_list = []

file = '../data/IN/in-tyler-names/MeasuresForJustice08CRHCriminalDefendantData.txt'
with open(file,'r') as infile1:
    next(infile1)
    for line in infile1:
        items = line.split(',')
        party_type = items[3].strip('"')
        if party_type == 'Defendant':           
            first = items[4]
            middle = items[5]
            last = items[6]
            suffix = items[7]
            name = ' '.join([last,first,middle,suffix])
            parse_result = parser.parse_name(name)
            name_list.append(name)
            result_list.append(parse_result)

runtime = time.time() - start_time 

#%%
print ("--- %s names per seconds ---" % str(len(name_list)/runtime))
#print (name_list[52])
#print (result_list[52])
