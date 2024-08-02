# Copyright 2024 Paride Azzari
#
# Licensed under the MIT License. See LICENSE

def start(folder_path: str = '.'):
    '''
    Give a folder path as a relative or absolute path, the script will analyze all the .csv files found in the directory and return a DataFrame containing the results.
    Leaving returns the Current Working Directory.
    '''
 
    from .files import TRAFolder
    
    results = TRAFolder(folder_path).analyze()
    results.to_csv('Analysis.csv')