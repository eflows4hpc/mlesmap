'''
STEP 2: SRF EXTRACTION WITH PYCOMPSS
In this step a database is generated in which the geographic coordinates of the synthetic station, the coordinates and depth of the hypocentre and the Euclidean distance and azimuth are displayed.
PyCompss has been used for this purpose.
From the file name we get the information related to the number of the synthesised station and the rupture, 
from the Sites file the information related to the coordinates of this station and from the srf files the 
information related to the earthquake. The azimuth and Euclidean distance are calculated separately.

In @task the databases of all Sources_IDs are obtained in parallel, for a PSA of 3sec and 5sec.
In def azimuth_3s and def azimuth_5s the azimuth, distance and plunge columns are obtained.
In def psa_export_csv the csv for 3s and 5s are exported for each synthetic station.
'''

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
def psa_start(path_to_folders):
    print(path_to_folders)
    f_Folders = []
    for (dirpath, dirnames, filenames) in walk(path_to_folders):
        f_Folders.extend(dirnames)
        break
    for nk in f_Folders:
        print(nk)
        path_to_file = path_to_folders+nk+'/'
        print(path_to_file)
    f_Stations = []
    for (dirpath, dirnames,filenames) in walk(path_to_file):
        f_Stations.extend(dirnames)
        break   
    for i in f_Stations:     #Creation of a database for each synthetic station and for each PSA and creation of the folder out.
        PSA_3s = pd.DataFrame()
        PSA_5s = pd.DataFrame()
        path_Stat = path_to_file+i+'/outputExtraction/'
        if not os.path.exists(path_Stat):
            continue

        folder_Out = path_Stat + 'PSA_output_PyCompss/'
        if not os.path.exists(folder_Out):
            os.mkdir(folder_Out)
        else:
            continue

#TASK
@task(folder_Out=FOLDER_OUT)  
def SS_psa(path_to_file, f_Stations):
    for i in f_Stations:
        PSA_3s = pd.DataFrame()
        PSA_5s = pd.DataFrame()
        path_Stat = path_to_file+i+'/outputExtraction/'
        if not os.path.exists(path_Stat):
            continue

        folder_Out = path_Stat + 'PSA_output_PyCompss/'
        if not os.path.exists(folder_Out):
            os.mkdir(folder_Out)
            print('se ha creado la carpeta PSA_output')
        else:
            continue   

        f_Files = []
        print('f_Files')
        for (dirpath, dirnames, filenames) in walk(path_Stat):
            f_Files.extend(filenames)
            break

        for j in f_Files:
            print(j)
            try:
                ij = j
                ij_split = ij.split('_')
                SS_csv = int(ij_split[4])  
                src_csv = int(ij_split[6])

                f = pd.read_csv(path_Stat + j)
                psa_db = pd.DataFrame()

                for k in range(len(f['Unnamed: 0'])):
                    print(k)
                    l = f['Unnamed: 0'].iloc[k]
                    ik_split = l.split('_')
                    psa_number = int(ik_split[2])

                    psa_db = psa_db.append({'SS': SS_csv,'Source_ID': src_csv ,'PSA': psa_number, 'PSA_max': f['PSA_max'].iloc[k],'RuptureVariation_ID': f['rv'].iloc[k]}, ignore_index=True)
                    
                    f3 = pd.read_csv('/path/to/CyberShake_Sites.csv')
                    data_site = {
                            'SS': (f3['CS_Site_ID'] - 1000),
                            'Site_Lat': (f3['CS_Site_Lat']),
                            'Site_Lon': (f3['CS_Site_Lon'])}
                    site_db = pd.DataFrame(data_site)

                    db_ss2 = pd.merge(psa_db, site_db, on = 'SS')

                    psa_3_db = db_ss2.query('PSA == 3')
                
                    psa_5_db = db_ss2.query('PSA == 5')

                    path_Test = path_to_file + i + '/srf_Test/'
                    f_Test = []
                    for (dirpath, dirnames, filenames) in walk(path_Test):
                        f_Test.extend(filenames) 

                    for m in f_Test:
                        try:
                            im = m
                            im_split = im.split('_')
                            SS_Test = int(im_split[2])
                            f2 = pd.read_csv(path_Test + m)


                            data_srf = {
                                    'SS': SS_Test,
                                    'Source_ID': (f2['Source_ID']),
                                    'Rupture_ID': (f2['Rupture_ID']),
                                    'RuptureVariation_ID': (f2['Rupture_Variation_ID'] +1),
                                    'Hypocenter_Lat': (f2['Lat_hypo']), 
                                    'Hypocenter_Lon': (f2['Lon_hypo']),
                                    'Hypocenter_Depth': (f2['Depth_hypo']).round(2),
                                    'Magnitude': (f2['Rupture_ID'] * 0.1).round(2)
                                    }
                            srf_db = pd.DataFrame(data_srf)
                            print(srf_db)
                        except: (' SRF folder does not exist')
                   
            
                db_ss1_3s = pd.merge(psa_3_db, srf_db, on = ['RuptureVariation_ID', 'Source_ID'])
                #print(db_ss1_3s)

                db_ss1_5s = pd.merge(psa_5_db, srf_db, on = ['RuptureVariation_ID', 'Source_ID'])
                #print(db_ss1_5s)

                PSA_3s = PSA_3s.append(db_ss1_3s)
                PSA_5s = PSA_5s.append(db_ss1_5s)
            except: print('ERROR')
        SS_str = str(SS_csv)


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

    PSA_3s = PSA_3s.drop(PSA_5s.index[16632:])
    PSA_5s = PSA_5s.drop(PSA_5s.index[16632:])

    PSA_3s.to_csv(folder_Out + 'PSA_3_SS_' + SS_str + '.csv' )
    PSA_5s.to_csv(folder_Out + 'PSA_5_SS_' + SS_str + '.csv' )

        
if __name__ == "__main__":
    path_to_folders = sys.argv[1]
    output_folder= sys.argv[2]
    psa_start(path_to_folders,output_folder)