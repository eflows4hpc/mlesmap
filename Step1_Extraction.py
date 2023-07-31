'''
Step 1: SYNTHETIC SEISMOGRAMS EXTRACTION

In this code the data extracted from CyberShake are processed. 

The code starts in the general folder where all the information is located, from here it walks through the folders until it reaches the level where the synthetic stations are located.
Inside the folder of each synthetic station a folder called outputExtraction is created where the outputs obtained from the execution of this code are stored.

Info in outputExtraction: PGA, PGV, PSA, PSV and SD max and average. Mw, src, rv
'''

from rotinv_maxavg import *
from read_seis_TEST import *
import numpy as np
import matplotlib.pyplot as plt
import numpy as np
import os
import pandas as pd
from os import walk

path_to_folders = '/path/to/folder'

f_Folders = []
for (dirpath, dirnames, filenames) in walk(path_to_folders):
  f_Folders.extend(dirnames)
  break

for nk in f_Folders:
  path_to_file = path_to_folders+nk+'/'

  f_Stations = []
  for (dirpath, dirnames, filenames) in walk(path_to_file):
    f_Stations.extend(dirnames)
    break

  for i in f_Stations:
    print(i)
    path_Stat = path_to_file+i+'/'
    folder_Out = path_Stat+'outputExtraction'
    print(path_Stat)
    os.makedirs(folder_Out, exist_ok=True)

    f_Files = []  # Contains the seismogram files  
    for (dirpath, dirnames, filenames) in walk(path_Stat+'post-processing/'):
      f_Files.extend(filenames)   
      break
    f_Seismograms = []
    for ik in f_Files:
      f2 = ik.split(".")
      try:
        if f2[1] == 'grm': 
          f_Seismograms.append(ik)
      except:
        print('ERROR_filenames')
    
    for j in f_Seismograms:
      try:
        path_Seismograms = path_Stat+'post-processing/'
        grm_file =  path_Seismograms+j
        f1 = j.split("_")    
        src = f1[4] 
        stat = f1[2] 
        f3 = f1[5].split(".")
        rup = f3[0]
        Mw = int(rup)*0.1    
        g        = 0.01        # CS units [cm/sec^2] ---> Avrg-RotI units [m/sec^2] 
        damp     = 0.05 

        periods  = np.asarray((1,2,3,5,7.5,10))  
        table_CS_Ruptures = '/path/to/Ruptures.csv'
        Tb_Ruptures     = pd.read_csv(table_CS_Ruptures)
        numb_ruptures = len(Tb_Ruptures.Source_ID)    
        seis = Seismogram(grm_file)
        seis.readData()

        dfUmax = pd.DataFrame()
        #print(seis.num_rvs)
        index_labels = []
        for k in range(0, seis.num_rvs):  #i = 0
          rv_id = seis.rvs[k]
          nt = seis.nt
          dt = seis.dt
          time = seis.dt*np.arange(0.5,seis.nt-0.5,1) 
          (x_data, y_data) = seis.data_dict[k]
          x_data = np.asarray(x_data)
          y_data = np.asarray(y_data)
          Ax = (1/dt)*(x_data[1:nt] - x_data[0:nt-1]); Ay = (1/dt)*(y_data[1:nt] - y_data[0:nt-1])

          Umax = rotinv_maxavg(Ax*g,Ay*g,dt,periods,damp)

          dir1 = 'rv_'+str(k+1)+'_1_s'
          dir2 = 'rv_'+str(k+1)+'_2_s'
          dir3 = 'rv_'+str(k+1)+'_3_s'
          dir4 = 'rv_'+str(k+1)+'_5_s'
          dir5 = 'rv_'+str(k+1)+'_7_s'
          dir6 = 'rv_'+str(k+1)+'_10_s'
          #print(dir2)
          index_labels.append(dir1)
          index_labels.append(dir2)    
          index_labels.append(dir3) 
          index_labels.append(dir4) 
          index_labels.append(dir5) 
          index_labels.append(dir6) 

          Umax['Mw'] = Mw*np.ones(len(Umax))
          Umax['src'] = int(src)*np.ones(len(Umax))
          Umax['rv'] = k*np.ones(len(Umax))+1
          Umax = Umax.set_axis(index_labels, axis='index')
          dfUmax =  dfUmax.append(Umax)  
          index_labels = []

        dfUmax.to_csv(folder_Out+'/RotI_PGA_PSA_stat_'+stat+'_src_'+src+'_rup_'+rup+'.csv') 
      except:print('post processing does not exist', i)

