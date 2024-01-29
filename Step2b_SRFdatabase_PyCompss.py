""" SRF DATABASE WITH PYCOMPSS

In this step a database is generated in which the geographic coordinates of the synthetic station, the coordinates and
depth of the hypocentre and the Euclidean distance and azimuth are displayed. PyCompss has been used for this purpose.
From the file name we get the information related to the number of the synthesised station and the rupture,
from the Sites file the information related to the coordinates of this station and from the srf files the
information related to the earthquake. The azimuth and Euclidean distance are calculated separately.

In @task the databases of all Sources_IDs are obtained in parallel, for the different periods.
In def azimuth_3s and def azimuth_5s the azimuth, distance and plunge columns are obtained.
In def psa_export_csv the csv for 3s and 5s are exported for each synthetic station.

cmd: nohup pycompss run Step2b_SRFdatabase_PyCompss.py /path/to/folders/ folder_Out & out.out &

Authors: Marisol Monterrubio Velasco and Rut Blanco Prieto (Last modification October 2023) 
-------------------------------------------------------------------------------------------------------------
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
from geopy.distance import geodesic
from geopy import Point
import math
import os
from os import walk
from pycompss.api.task import task
from pycompss.api.parameter import *
import sys	

#MAIN
def psa_start(path_to_folders,output_folder):
    print(path_to_folders)
    f_Folders = []
    for (dirpath, dirnames, filenames) in walk(path_to_folders):
        f_Folders.extend(dirnames)
        break
    for nk in f_Folders[0:1]:
        print(nk)
        path_to_file = path_to_folders+nk+'/'
        print(path_to_file)
        f_Stations = []
        for (dirpath, dirnames,filenames) in walk(path_to_file):
            f_Stations.extend(dirnames)
            break
        for i in f_Stations:   
            path_Stat = path_to_file+i+'/PSAoutputExtraction/'
            path_srf = path_to_file+i+'/PSAsrfExtraction/'
            if not os.path.exists(path_Stat):
                print('There is not a PSAoutputExtraction folder in :' + path_to_file+i)
                continue

            folder_Out = path_to_file + i + '/' + output_folder
            os.makedirs(folder_Out, exist_ok=True)

            f_Files = []
            for (dirpath, dirnames, filenames) in walk(path_Stat):
                f_Files.extend(filenames)
                break
            CyberS_sites_temp = (
                    "/data/to/inputData/CyberShake_Sites.csv"
                )
            f_stat = i.split("_")
            stat = f_stat[1]

            name_Out1 = folder_Out + '/PSA_1_SS_' + stat + '.csv' 
            name_Out2 = folder_Out + '/PSA_2_SS_' + stat + '.csv'
            name_Out3 = folder_Out + '/PSA_3_SS_' + stat + '.csv'
            name_Out5 = folder_Out + '/PSA_5_SS_' + stat + '.csv'
            name_Out7 = folder_Out + '/PSA_7_SS_' + stat + '.csv'
            name_Out10 = folder_Out + '/PSA_10_SS_' + stat + '.csv'

            SS_psa(path_Stat,path_srf,f_Files,CyberS_sites_temp,name_Out1,name_Out2,name_Out3,name_Out5,name_Out7,name_Out10)


#TASK
@task(path_Stat=FILE_IN,path_srf=FILE_IN,f_Files=COLLECTION_FILE_IN,CyberS_sites_temp=FILE_IN,name_Out1=FILE_OUT,name_Out2=FILE_OUT,name_Out3=FILE_OUT,name_Out5=FILE_OUT,name_Out7=FILE_OUT,name_Out10=FILE_OUT) 
def SS_psa(path_Stat,path_srf,f_Files,CyberS_sites_temp,name_Out1,name_Out2,name_Out3,name_Out5,name_Out7,name_Out10):
    print('ENTRE:',path_Stat)
    PSA_1s = pd.DataFrame()
    PSA_2s = pd.DataFrame()
    PSA_3s = pd.DataFrame()
    PSA_5s = pd.DataFrame()
    PSA_7s = pd.DataFrame()
    PSA_10s = pd.DataFrame()
    srf_db = pd.DataFrame()
    f_Files = []
    for (dirpath, dirnames, filenames) in walk(path_Stat):
        f_Files.extend(filenames)
        break
    for j in f_Files:
        print(j)
        ij = j
        ij_split = ij.split('_')
        SS_csv = int(ij_split[4])
        src_csv = int(ij_split[6])
        psa_stat_temp = path_Stat + j
        f = pd.read_csv(psa_stat_temp)
        psa_db = pd.DataFrame()

        for k in range(len(f['Unnamed: 0'])):
            print(k)
            l = f['Unnamed: 0'].iloc[k]
            ik_split = l.split('_')
            psa_number = int(ik_split[2])

            psa_db = psa_db.append({'SS': SS_csv,'Source_ID': src_csv ,'PSA': psa_number, 'PSA_max': f['PSA_max'].iloc[k],'Rupture_Variation_ID': f['rv'].iloc[k]}, ignore_index=True)

            f3 = pd.read_csv(CyberS_sites_temp)
            data_site = {
                    'SS': (f3['CS_Site_ID'] - 1000),
                    'Site_Lat': (f3['CS_Site_Lat']),
                    'Site_Lon': (f3['CS_Site_Lon'])}
            site_db = pd.DataFrame(data_site)

            db_ss2 = pd.merge(psa_db, site_db, on = 'SS')

            psa_1_db = db_ss2.query('PSA == 1')
            psa_2_db = db_ss2.query('PSA == 2')
            psa_3_db = db_ss2.query('PSA == 3')
            psa_5_db = db_ss2.query('PSA == 5')
            psa_7_db = db_ss2.query('PSA == 7')
            psa_10_db = db_ss2.query('PSA == 10')

            f_Test = []
            for (dirpath, dirnames, filenames) in walk(path_srf):
                f_Test.extend(filenames)

            print(f_Test)
            for m in f_Test:
                im = m
                im_split = im.split('_')
                print('im_split', im_split)
                SS_Test = int(im_split[2])
                f2 = pd.read_csv(path_srf + m)
                print('f2', f2.head(5))
                data_srf = {
                            'SS': SS_Test,
                            'Source_ID': (f2['Source_ID']),
                            'Rupture_ID': (f2['Rupture_ID']),
                            'Rupture_Variation_ID': (f2['Rupture_Variation_ID'] ),   #,Rupture_Variation_ID    (+1)
                            'Hypocenter_Lat': (f2['Lat_hypo']),
                            'Hypocenter_Lon': (f2['Lon_hypo']),
                            'Hypocenter_Depth': (f2['Depth_hypo']).round(2),
                            'Magnitude': (f2['Rupture_ID'] * 0.1).round(2)
                            }
                srf_db = pd.DataFrame(data_srf)

        db_ss1_1s = pd.merge(psa_1_db, srf_db, on = ['Rupture_Variation_ID', 'Source_ID'])
        db_ss1_2s = pd.merge(psa_2_db, srf_db, on = ['Rupture_Variation_ID', 'Source_ID'])
        db_ss1_3s = pd.merge(psa_3_db, srf_db, on = ['Rupture_Variation_ID', 'Source_ID'])
        db_ss1_5s = pd.merge(psa_5_db, srf_db, on = ['Rupture_Variation_ID', 'Source_ID'])
        db_ss1_7s = pd.merge(psa_7_db, srf_db, on = ['Rupture_Variation_ID', 'Source_ID'])
        db_ss1_10s = pd.merge(psa_10_db, srf_db, on = ['Rupture_Variation_ID', 'Source_ID'])

        PSA_1s = PSA_3s.append(db_ss1_1s)
        PSA_2s = PSA_5s.append(db_ss1_2s)
        PSA_3s = PSA_5s.append(db_ss1_3s)
        PSA_5s = PSA_5s.append(db_ss1_5s)
        PSA_7s = PSA_5s.append(db_ss1_7s)
        PSA_10s = PSA_5s.append(db_ss1_10s)

    SS_str = str(SS_csv)

    PSA_1s['Eu_distance'] = 0
    PSA_1s['Azimuth'] = 0
    PSA_1s['Plunge'] = 0
    for r in range(len(PSA_1s)):

        x1,y1,z1 = PSA_1s['Hypocenter_Lat'].iloc[r], PSA_1s['Hypocenter_Lon'].iloc[r], PSA_1s['Hypocenter_Depth'].iloc[r]
        start = Point(PSA_1s['Hypocenter_Lat'].iloc[r], PSA_1s['Hypocenter_Lon'].iloc[r])
        x2,y2,z2 = PSA_1s['Site_Lat'].iloc[r], PSA_1s['Site_Lon'].iloc[r],0
        end = Point(PSA_1s['Site_Lat'].iloc[r], PSA_1s['Site_Lon'].iloc[r])

        distance = (geodesic(start, end).km)
        azimuth = (math.degrees(math.atan2((x2-x1),(y2-y1))))
        plunge = (math.degrees(math.asin((z1)/geodesic(start, end).km)))

        PSA_1s.loc[r, 'Eu_distance'] = distance
        PSA_1s.loc[r, 'Azimuth'] = azimuth
        PSA_1s.loc[r, 'Plunge'] = plunge

    PSA_2s['Eu_distance'] = 0
    PSA_2s['Azimuth'] = 0
    PSA_2s['Plunge'] = 0
    for w in range(len(PSA_2s)):

        x1,y1,z1 = PSA_2s['Hypocenter_Lat'].iloc[w], PSA_2s['Hypocenter_Lon'].iloc[w], PSA_2s['Hypocenter_Depth'].iloc[w]
        start = Point(PSA_2s['Hypocenter_Lat'].iloc[w], PSA_2s['Hypocenter_Lon'].iloc[w])
        x2,y2,z2 = PSA_2s['Site_Lat'].iloc[w], PSA_2s['Site_Lon'].iloc[w],0
        end = Point(PSA_2s['Site_Lat'].iloc[w], PSA_2s['Site_Lon'].iloc[w])

        distance = (geodesic(start, end).km)
        azimuth = (math.degrees(math.atan2((x2-x1),(y2-y1))))
        plunge = (math.degrees(math.asin((z1)/geodesic(start, end).km)))

        PSA_2s.loc[w, 'Eu_distance'] = distance
        PSA_2s.loc[w, 'Azimuth'] = azimuth
        PSA_2s.loc[w, 'Plunge'] = plunge


    PSA_3s['Eu_distance'] = 0
    PSA_3s['Azimuth'] = 0
    PSA_3s['Plunge'] = 0
    for n in range(len(PSA_3s)):

        x1,y1,z1 = PSA_3s['Hypocenter_Lat'].iloc[n], PSA_3s['Hypocenter_Lon'].iloc[n], PSA_3s['Hypocenter_Depth'].iloc[n]
        start = Point(PSA_3s['Hypocenter_Lat'].iloc[n], PSA_3s['Hypocenter_Lon'].iloc[n])
        x2,y2,z2 = PSA_3s['Site_Lat'].iloc[n], PSA_3s['Site_Lon'].iloc[n],0
        end = Point(PSA_3s['Site_Lat'].iloc[n], PSA_3s['Site_Lon'].iloc[n])

        distance = (geodesic(start, end).km)
        azimuth = (math.degrees(math.atan2((x2-x1),(y2-y1))))
        plunge = (math.degrees(math.asin((z1)/geodesic(start, end).km)))

        PSA_3s.loc[n, 'Eu_distance'] = distance
        PSA_3s.loc[n, 'Azimuth'] = azimuth
        PSA_3s.loc[n, 'Plunge'] = plunge


    PSA_5s['Eu_distance'] = 0
    PSA_5s['Azimuth'] = 0
    PSA_5s['Plunge'] = 0
    for o in range(len(PSA_5s)):

        x1,y1,z1 = PSA_5s['Hypocenter_Lat'].iloc[o], PSA_5s['Hypocenter_Lon'].iloc[o], PSA_5s['Hypocenter_Depth'].iloc[o]
        start = Point(PSA_5s['Hypocenter_Lat'].iloc[o], PSA_5s['Hypocenter_Lon'].iloc[o])
        x2,y2,z2 = PSA_5s['Site_Lat'].iloc[o], PSA_5s['Site_Lon'].iloc[o],0
        end = Point(PSA_5s['Site_Lat'].iloc[o], PSA_5s['Site_Lon'].iloc[o])

        distance = (geodesic(start, end).km)
        azimuth = (math.degrees(math.atan2((x2-x1),(y2-y1))))
        plunge = (math.degrees(math.asin((z1)/geodesic(start, end).km)))

        PSA_5s.loc[o, 'Eu_distance'] = distance
        PSA_5s.loc[o, 'Azimuth'] = azimuth
        PSA_5s.loc[o, 'Plunge'] = plunge

    
    PSA_7s['Eu_distance'] = 0
    PSA_7s['Azimuth'] = 0
    PSA_7s['Plunge'] = 0
    for u in range(len(PSA_7s)):

        x1,y1,z1 = PSA_7s['Hypocenter_Lat'].iloc[u], PSA_7s['Hypocenter_Lon'].iloc[u], PSA_7s['Hypocenter_Depth'].iloc[u]
        start = Point(PSA_7s['Hypocenter_Lat'].iloc[u], PSA_7s['Hypocenter_Lon'].iloc[u])
        x2,y2,z2 = PSA_7s['Site_Lat'].iloc[u], PSA_7s['Site_Lon'].iloc[u],0
        end = Point(PSA_7s['Site_Lat'].iloc[u], PSA_7s['Site_Lon'].iloc[u])

        distance = (geodesic(start, end).km)
        azimuth = (math.degrees(math.atan2((x2-x1),(y2-y1))))
        plunge = (math.degrees(math.asin((z1)/geodesic(start, end).km)))

        PSA_7s.loc[u, 'Eu_distance'] = distance
        PSA_7s.loc[u, 'Azimuth'] = azimuth
        PSA_7s.loc[u, 'Plunge'] = plunge

    
    PSA_10s['Eu_distance'] = 0
    PSA_10s['Azimuth'] = 0
    PSA_10s['Plunge'] = 0
    for p in range(len(PSA_10s)):

        x1,y1,z1 = PSA_10s['Hypocenter_Lat'].iloc[p], PSA_10s['Hypocenter_Lon'].iloc[p], PSA_10s['Hypocenter_Depth'].iloc[p]
        start = Point(PSA_10s['Hypocenter_Lat'].iloc[p], PSA_10s['Hypocenter_Lon'].iloc[p])
        x2,y2,z2 = PSA_10s['Site_Lat'].iloc[p], PSA_10s['Site_Lon'].iloc[p],0
        end = Point(PSA_10s['Site_Lat'].iloc[p], PSA_10s['Site_Lon'].iloc[p])

        distance = (geodesic(start, end).km)
        azimuth = (math.degrees(math.atan2((x2-x1),(y2-y1))))
        plunge = (math.degrees(math.asin((z1)/geodesic(start, end).km)))

        PSA_10s.loc[p, 'Eu_distance'] = distance
        PSA_10s.loc[p, 'Azimuth'] = azimuth
        PSA_10s.loc[p, 'Plunge'] = plunge

    PSA_1s = PSA_1s.drop(PSA_5s.index[16632:]) #number of events
    PSA_2s = PSA_2s.drop(PSA_5s.index[16632:])
    PSA_3s = PSA_3s.drop(PSA_5s.index[16632:])
    PSA_5s = PSA_5s.drop(PSA_5s.index[16632:])
    PSA_7s = PSA_7s.drop(PSA_5s.index[16632:])
    PSA_10s = PSA_10s.drop(PSA_5s.index[16632:])

    PSA_1s.to_csv(name_Out1)
    PSA_2s.to_csv(name_Out2)
    PSA_3s.to_csv(name_Out3)
    PSA_5s.to_csv(name_Out5)
    PSA_7s.to_csv(name_Out7)
    PSA_10s.to_csv(name_Out10)


if __name__ == "__main__":
    path_to_folders = sys.argv[1]
    output_folder= sys.argv[2]
    psa_start(path_to_folders,output_folder)
