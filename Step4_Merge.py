'''
STEP 4: MERGE DATABASE
Join the databases obtained in the previous step for each station into a general one for each PSA in a folder colled PSA_merge
------------------------------------------------------------------------------------------------------------------------------
Copyright (c) . All rights reserved.

Redistribution and use in source and binary forms, with or without modification, are permitted provided that the following conditions are met:

1. Redistributions of source code must retain the above copyright notice, this list of conditions and the following disclaimer.

2. Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following disclaimer in the documentation
and/or other materials provided with the distribution.

3. Neither the name of the copyright holder nor the names of its contributors may be used to endorse or promote products derived from this software without 
specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED 
WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY 
DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS 
OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING 
NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
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
            
    

