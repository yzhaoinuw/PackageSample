#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May  5 21:23:43 2020

@author: yue
"""

import os
import pkg_resources

import torch
from flair.data import Sentence
from flair.models import SequenceTagger

#%%  

symbols = '!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~'

def validate(name):
    ''' a valid name (person's or entity's) must be a string that 
    containsat least one letter, and maybe some approved symbols '''
    if not isinstance(name,str):
        return False
    name = name.translate(str.maketrans('','',symbols))
    name = ''.join(name.split())
    if name.isalnum() or len(name) == 0:
        return True
    return False

def process_name(name):
    ''' used for creating training data '''
    name = name.translate(str.maketrans('', '', '".'))
    for char in name.lower():
        if char in symbols:
            # string.replace() is faster than re.sub()
            # https://stackoverflow.com/questions/5668947/use-pythons-string-replace-vs-re-sub
            name = name.replace(char,' '+char+' ')   
    name = ' '.join(name.split()) 
    name = name.lower()
    return name 

class NameParser():
    def __init__(self,model_name=None):
        model_source = pkg_resources.resource_filename('MFJ', 'model/')
        if model_name is None:
            model_name = 'name_parser_elmo_noncrf'
            self.model_path = os.path.join(model_source,os.path.join(model_name,'best-model.pt'))
            assert (os.path.exists(self.model_path)), "Did not find the default model, \
                please provide a model name."
        else:
            self.model_path = os.path.join(model_source,os.path.join(model_name,'best-model.pt'))
        self.model = SequenceTagger.load(self.model_path)
        # only for flair 0.5 version
        #self.model.embeddings.embedding_mode_fn = lambda x: torch.cat(x, 0)
        if torch.cuda.is_available():
            self.model.embeddings.ee.cuda_device = 0
        else:
            self.model.embeddings.ee.cuda_device = -1  
        
    def parse_name(self,name):
        if not validate(name):
            raise TypeError("a valid name (person's or entity's) must be a \
                            string that containsat least one letter")
        name = process_name(name)
        name = Sentence(name)
        self.model.predict(name,all_tag_prob=False)
        results = {}
        #print (processed_name)
        #print (name.tokens[2].text)
        #return name.to_dict(tag_type='ner')
        for part in name.get_spans('ner'):
            label = part.tag
            text = ' '.join([t.text for t in part.tokens])
            score = part.score
            if label in results:
                #label = label+"'"
                results[label][0] += ' '+text
                results[label][1] = min(results[label][1],score)
            else:    
                results[label] = [text,score]
        return results  
     
    
