#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May 21 21:32:43 2020

@author: yue
"""

import pkg_resources

path = 'shelter_detection/resources/shelter_list.db'
db_path = pkg_resources.resource_filename('MFJ', path)
