import os
import pandas as pd


def create_dir(full_path):
    """create a new path where if it doesn't already exist"""
    if not os.path.exists(full_path):
        os.makedirs(full_path)
        print('created directory ' + full_path)
    else:
        print('path already exists: ' + full_path)



def join_csv(path, file_list=None, wildcard='',return_as='df'):
    
    """
    join multiple csv files:
        
       > join_csv(path, file_list=None, wildcard='', return_as='df')

       - supply file_list or read from path as default
       - provide direct wildcard (ie no need for *) to filter based on 
         filename pattern
       - return_as 'df' or 'dict'

    """

    dict_store = {} 
    
    if file_list is None:
        dir_contents = os.listdir(path)
        filenames = [f for f in  dir_contents if os.path.isfile(path / f)] 

    else:
        filenames = file_list
    
    filenames = [f for f in filenames if wildcard in f]
    
    for file in filenames:
        _this_file = pd.read_csv(path / file, low_memory=False)
        _this_file['source_file'] = file
        dict_store[file] = _this_file

        print('>>> ' + file, _this_file.shape)

        
    if return_as == 'dict':
        return dict_store
    
    else:
        return pd.concat(dict_store).reset_index(drop=True)

