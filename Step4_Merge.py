'''
STEP 4: MERGE DATABASE
Join the databases obtained in the previous step for each station into a general one for each PSA in a folder colled PSA_merge
'''

import pandas as pd
import numpy as np
import os
from os import walk

path_to_folders = '/path/to/folder/'
path1 = '/data/'
f_Folders = []
for (dirpath, dirnames, filenames) in walk(path_to_folders):
    f_Folders.extend(dirnames)
    break
PSA_3s = pd.DataFrame()
PSA_5s = pd.DataFrame()

for nk in f_Folders: 
    folder_out = path1 + 'PSA_merge/'   
    if not os.path.exists(folder_out):
        os.mkdir(folder_out)
 
    path_to_file = path_to_folders + 'nk/'
    
    f_Stations = []
    for (dirpath, dirnames,filenames) in walk(path_to_file):
        f_Stations.extend(dirnames)
        break

    for i in f_Stations:
        print('i:', i)
        path_Stat = path_to_file + i +'/outputExtraction/PSA_output/'
        print(path_Stat)

        f_Files = []
        for (dirpath, dirnames, filenames) in walk(path_Stat):
            f_Files.extend(filenames)
            break

        for j in f_Files:
            print('j:', j)
            ij = j
            ij_split = ij.split('_')
            PSA_num = int(ij_split[1])
            SS = ij_split[3]
            print(path_Stat + j)
            print('num psa:', PSA_num)

            if PSA_num == 5:
                f1 = pd.read_csv(path_Stat + j)
                PSA_5s = pd.concat([PSA_5s, f1])
            elif PSA_num == 3:
                f2 = pd.read_csv(path_Stat + j)
                PSA_3s = pd.concat([PSA_3s, f2])

            else:
                print("In station", i, "file", j, "is not a CSV file or is PSA 3sec")

            
            PSA_3s.to_csv(folder_out + 'PSA_3.csv' )
            PSA_5s.to_csv(folder_out + 'PSA_5.csv' )
            
    

