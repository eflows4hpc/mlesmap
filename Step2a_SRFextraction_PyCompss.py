""" SRF EXTRACTION
Extract from the .srf file the information related to the earthquake hypocentre, as well as the
rupture point identification and the ELON, ELAT, DTOP, SHYP, DHYP data.

cmd: nohup pycompss run Step2a_SRFextraction_PyCompss.py /path/to/data/ FolderOut &> out.out &

Author: Marisol Monterrubio (Last modification September 2023) 
----------------------------------------------------------------------------------------------
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
"""

import numpy as np
import pandas as pd
import utm
import os
from os import walk
from pycompss.api.task import task
from pycompss.api.parameter import *
import sys

def step_srf(path_to_folders,output_folder):
    print(path_to_folders)
    f_Folders = []
    for (dirpath, dirnames, filenames) in walk(path_to_folders):
        f_Folders.extend(dirnames)
        break
    for nk in f_Folders[:]:
        path_to_file = path_to_folders+nk+'/'
        f_Stations = []
        for (dirpath, dirnames, filenames) in walk(path_to_file):
            f_Stations.extend(dirnames)
            break
        for i in f_Stations:  # Loop that goes through the stations

            path_Stat = path_to_file+i+'/'
            folder_Out = path_Stat+output_folder
            os.mkdir(folder_Out)
            try:
                f_stat = i.split('_')
                stat = f_stat[1]
                name_Out = folder_Out+'/srf_extraction_'+stat+'_src.csv'
                flag = os.path.exists(path_Stat+'post-processing')
                if flag == True:
                    compute_srf(path_Stat,folder_Out,name_Out)
            except:
                continue
                print('ERROR_STATION',i)

@task(name_Out=FILE_OUT)
def compute_srf(path_Stat,folder_Out,name_Out):
    f_Files = []    # Contains the seismogram files
    for (dirpath,dirnames, filenames) in walk(path_Stat+'post-processing/'):
        f_Files.extend(filenames)
        break
    f_SRF = []
    for ik in f_Files:
        try:
            f2 = ik.split(".")
            if f2[3] == 'srf':
                f_SRF.append(path_Stat+'post-processing/'+ik)
        except:
            R = 1+1
    if f_SRF != []:
        srf_out_station = srf_station_extraction(f_SRF)
        print(len(srf_out_station),srf_out_station.iloc[0])
    else:
         print('station-no-post-pro',folder_Out)
         srf_out_station = pd.DataFrame()
    srf_out_station.to_csv(name_Out)

def srf_station_extraction(f_SRF):
    srf_out_station = pd.DataFrame()
    for srf_file in f_SRF:
        srf_out = srf_extraction(srf_file)
        srf_out_station = srf_out_station.append(srf_out, ignore_index=True)
    return srf_out_station

def srf_extraction(srf_file2):
    srf_temp =  os.path.basename(srf_file2)
    srf_file = srf_temp
    my_file = pd.read_table(srf_file2)
    df1 = my_file.iloc[1]              # first row data extraction
    df2 = df1.str.split( )          # split first row data by space
    df3 = my_file.iloc[2]              # second row data extraction
    df4 = df3.str.split( )
    data = {'ELON': [float(df2.iloc[0][0])],
            'ELAT': [float(df2.iloc[0][1])],
            'DTOP': [float(df4.iloc[0][2])],
            'SHYP': [float(df4.iloc[0][3])],
            'DHYP': [float(df4.iloc[0][4])]}
    srf = pd.DataFrame(data)
    x_hypo, y_hypo, utm_number, utm_letter = utm.from_latlon((srf['ELAT']).values, (srf['ELON']).values)
    y_hypo += 1000.0 * srf['SHYP'].values
    Lat_hypo, Lon_hypo = utm.to_latlon(x_hypo, y_hypo,utm_number, utm_letter)
    Depth_hypo = srf['DTOP'].values + srf['DHYP'].values
    #print(srf_file)
    f = srf_file.split("_")
    f2 = f[3].split(".")
    f3 = f[4].split("s")
    data_final = {'Source_ID': [int(f[2])],
                  'Rupture_ID': [int(f2[0])],
                  'Rupture_Variation_ID':[int(f3[1])],
                  'Lat_hypo': [float(Lat_hypo)],
                  'Lon_hypo': [float(Lon_hypo)],
                  'Depth_hypo': [float(Depth_hypo)]}
    srf_return = pd.DataFrame(data_final)
    srf_out = pd.concat([srf_return, srf], axis=1)
    return srf_out

if __name__ == "__main__":
    path_to_folders = sys.argv[1]
    output_folder= sys.argv[2]
    step_srf(path_to_folders,output_folder)

