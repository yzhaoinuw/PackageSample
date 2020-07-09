#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun  4 01:57:42 2020

@author: yue
"""

import os
import argparse

from flair.data import Corpus
from flair.datasets import ColumnCorpus
from flair.trainers import ModelTrainer
from flair.models import SequenceTagger

#%%
def continue_train(load_model_path,corpus,save_model_path):
    model_name = os.path.basename(os.path.normpath(save_model_path))
    ner_model = SequenceTagger.load(os.path.join(load_model_path,'best-model.pt'))
    trainer: ModelTrainer = ModelTrainer(ner_model, corpus)
    trainer.train(save_model_path,
                  learning_rate=0.1,
                  mini_batch_size=128,
                  max_epochs=3,
                  embeddings_storage_mode='none',
                  checkpoint=False)
    return ('continue training '+model_name+' complete.')

#%%
def main():     
    parser = argparse.ArgumentParser()
    parser.add_argument("load_model_path", 
                            help="path to the model folder",
                            )
    parser.add_argument("dataset_path", 
                            help="path to the dataset",
                            )
    parser.add_argument("--save_model_path",
                        help="where to save the new model, default to overwrite the \
                        original model",
                        )
    args = parser.parse_args()
    load_model_path = args.load_model_path
    save_model_path = args.save_model_path
    if save_model_path is None:
        save_model_path = load_model_path
    # this is the folder in which train, test and dev files reside
    data_folder = args.dataset_path
    # define columns
    columns = {0: 'text', 1: 'ner'}
    # init a corpus using column format, data folder and the names of the train, dev and test files
    corpus: Corpus = ColumnCorpus(data_folder, columns,
                                  train_file='train.txt',
                                  test_file='test.txt',
                                  dev_file='dev.txt',
                                  #column_delimiter='\t',
                                  in_memory=True)    
    continue_train(load_model_path,corpus,save_model_path)

#%%
if __name__ == "__main__":
    main()    