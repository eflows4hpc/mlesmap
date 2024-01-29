""" STEP 3: PLOT
Extract information to plot all the results together per magnitude also including the GMPEs
Author: Marisol Monterrubio (Last modification March 2023) 
-------------------------------------------------------------------------------------------------
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

import pandas as pd
import numpy as np
import os
from os import walk
from scipy.io import loadmat  # this is the SciPy module that loads mat-files
import matplotlib.pyplot as plt
from datetime import datetime, date, time
from R_BJ_from_CS_Site_Ruptures import *
from IcelandBayesGMMsPlots_OR import *
import pickle



path_to_file = '/path/to/file/'
path_to_stations = '/path/to/station/'

f_Files = []
for (dirpath, dirnames, filenames) in walk(path_to_stations):
  if dirnames != 'ResultsStep2':
    f_Files.extend(dirnames)
    break
  
STATIONs = len(f_Files) 
 
fs    = 8; lw = 1.0
g     = 1.0/9.81        #  To plot CS PGA/PSA [g: units]           
STAT  = 'ALL'           #  'ALL' (RV's); 'max'(LV); 'median'; 'mean'
ERROR = 'NO'            #  'YES', 'NO' 


table_CS_Ruptures = '/path/to/Ruptures.csv'
Tb_Ruptures     = pd.read_csv(table_CS_Ruptures)

rupture_NUMBER  = len(Tb_Ruptures)         # How many (Fault,Rupture-ID/Mw)'s have been modeled
Sources         = Tb_Ruptures.Source_ID    # Each modeled source/FAULT ID (to be read/#printed) 
Ruptures        = Tb_Ruptures.Rupture_ID   # Each modeled rupture/MW ID (to be read/#printed) 
Mws             = Tb_Ruptures.Mag          # Each modeled MW value


Mw_range      = np.unique(Mws)   
ALL_Mws  = len(Mw_range)                   # Mw_ind  = 1:ALL_Mws; 
rupture_range = np.unique(Ruptures)        # ID (integer) associated to Mw (real) 

numb_per  = 1
RVs = 24                                   # Max number of Rupture Variations for CS runs in SISZ.
 
PPeriods  = [3.] # %5.]'
contFiles = 0
Period_to_print = PPeriods[0]

if Period_to_print == 3.0:
  T = 3
  ip = 0 
elif Period_to_print == 5.0:
  T = 5
  ip = 1 
  
PSAtemp = np.empty((len(Sources),RVs))
PSAtemp[:] = np.NaN 
PGAtemp = np.empty((len(Sources),RVs))
PGAtemp[:] = np.NaN

for i_Mw in np.arange(len(Mw_range)):

  Mw = Mw_range[i_Mw]
  rupt_ID = rupture_range[i_Mw]
  with open(path_to_file+'Mw_'+str(rupt_ID)+'_RVs_per_src','rb') as f: 
    RVs_per_src = pickle.load(f)        
  with open(path_to_file+'Mw_'+str(rupt_ID)+'_PSA','rb') as f2: 
    PSA = pickle.load(f2)      
  ind = Ruptures[Ruptures == rupt_ID]     # ALL sources/FAULTS generating a Mw event(== rupt_ID): numb_srcs_for_Mw is the TOTAL number
  srcs_for_Mw = Sources[ind.index]
  numb_srcs_for_Mw = len(srcs_for_Mw)
  RJB_max = 300.        
  fig, ax = plt.subplots(1, 1)
 
  f,lstrGMMs,R,sigmaSamin,sigmaSamax = IcelandBayesGMMsPlots_OR(Period_to_print,Mw,RJB_max,ax)   
  f_Seismograms = []
  for ikr in f_Files:
    try:     
      f2 = ikr.split("_")

      f_Seismograms.append(f2[1])     
    except:
      print('ERROR_filenames') 
  for jj in np.arange(len(f_Seismograms)):  

    IDstation = str(f_Seismograms[jj])

    site_ID = 1000+int(f_Seismograms[jj])

    table = '/path/to/CyberShake_Site_Ruptures.csv'
    Sources_to_Site,R_BJ = R_BJ_from_CS_Site_Ruptures(table,site_ID)   

    indexStation = jj 
   
    if STAT == 'ALL':    
      for ij in np.arange(numb_srcs_for_Mw):             # INNER loop: For a given Mw process ALL FAULTS (srcs) that support such Mw                         
        src = srcs_for_Mw.iloc[ij]     
        contFiles =  contFiles+1                         # R_BJ distance from SITE_ID to current src
        ind2 = np.where(Sources_to_Site == src)
        R_BJ_to_src = R_BJ[ind2]
        PSAtemp[src-1,0:int(RVs_per_src[indexStation,src-1])] = PSA[indexStation,src-1,ip,0:int(RVs_per_src[indexStation,src-1])]       
        ax.loglog(R_BJ_to_src*np.ones(int(RVs_per_src[indexStation,src-1])),PSAtemp[src-1,0:int(RVs_per_src[indexStation,src-1])]*g,'ok',markersize=2)               
  plt.xlabel('Horizontal Distance to Fault ({\itR}_{JB}, km)',fontsize=fs)    
  if T==0:
    plt.ylabel('Peak Ground Acceleration (g)',fontsize=fs)
  else:
    plt.ylabel('Pseudo-spectra Acceleration (g) (T=' + str(T) + 's)',fontsize=fs)
  ax.set_aspect('equal', 'box')
  ax.grid(which='minor')
  lstrGMMs.append('CyberShake')
  plt.legend(lstrGMMs)
  plt.savefig(path_to_file+'T'+str(T)+'_Mw'+str(Mw)+'_Plot.png')
