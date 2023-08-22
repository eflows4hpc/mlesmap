import numpy as np
import pandas as pd
import scipy
from LIDA import *
from Rot2CompCW_rad import *
from tButterFilt import *
from scipy.linalg import lstsq, solve

def rotinv_maxavg(a1,a2,dt,periods,damp):
  
#%Script to Python Marisol Monterrubio 13/2/2023

#%PURPOSE: Calculate max and mean of PGA, PGV, PSA, PSV and SD
#%          using the method of:
#% Rupakhety and Sigbjornsson, 2013, 
#% "Rotation-invariant measures of earthquake response spectra",
#% Bull Earthquake Eng (2013) 11:1885–1893
#%--------------------------------------------------------------------------
#% INPUT: 
#%        a1,a2 = two horizontal acceleration time series amplitudes
#%        dt    = sampling interval [sec]
#%        periods = vector of requested oscillator periods [sec]
#%        damp  = fractional oscillator damping (e.g.: 0.05)
#%
#% OUTPUT:
#%    Umax  = struct of PGA, PGV, PSA, PSV and SD, rot.inv. maximum
#%    Uavg  = as Umax, but rotation invariant average values, which
#%            roughly correspond to GMRotD50 (see ref. paper above)
#%
#% 2019-02-08 Tim: Created.
#% 2019-03-10 Tim: 
#%   + Allowing selection of only PGA, when 'periods' is empty or zero.
#%   + Added Mean-removal, no longer corrected input required.
  periods = np.asarray(periods)
  Nper = np.size(periods)
  #% remove mean of traces:
  nt = np.size(a1);
  #print('a1',sum(a1))
  a1 = a1-sum(a1)/nt;
  #print(sum(a1),nt)
  #print('a2',sum(a2))
  a2 = a2-sum(a2)/nt;
  #print(sum(a2),nt)
  #% check requested periods: either just PGA/PGV, or also PSA/PSV/SD
  if (Nper==0): #% no PSA, PSV, SD, just PGA, PGV
      PSVmax=[];
      PSAmax=[];
      PSVavg=[];
      PSAavg=[];
      SDmax=[];
      SDavg=[];
  elif (Nper==1) and (periods==0):
      PSVmax=[];
      PSAmax=[];
      PSVavg=[];
      PSAavg=[];
      SDmax=[];
      SDavg=[];
  else: #% calc PSA, PSV and SD at requested periods
      omega=2*np.pi/periods;
      #% set initial conditions
      u0=0;
      ut0=0;
      rinf=1; #% mid-point rule a-form algorithm
      #% malloc
      SDmax = np.zeros(Nper)
      SDavg = np.zeros(Nper)
      for j in np.arange(Nper):
          #% lin.el.SDOF dis.responses:
          #print(dt,a1,omega[j],damp,u0,ut0,rinf)
          u1, u1t, u1tt = LIDA(dt,a1,omega[j],damp,u0,ut0,rinf); 
          #print('u1#####################', u1[0:100])
          u2, u2t, u2tt = LIDA(dt,a2,omega[j],damp,u0,ut0,rinf);
          #print('u2####################', u2[0:100])
          #print((u1**2) + (u2**2))
          SDmax[j] = np.max(np.sqrt(u1**2 + u2**2)); #% rotation invariant max
          #print('SDmax', SDmax)         
          #% ordinary LSQ, get principal component angle:
          #print('u1',np.dot(np.transpose(u1),u1))
          #print('trans', np.dot(np.transpose(u1),u2))          
          ji = solve(np.dot(np.transpose(u1),u1),np.dot(np.transpose(u1),u2))
          #print('ji', ji)
          rad = np.arctan(ji);
          #print('rad', rad)                   
          d1,d2 = Rot2CompCW_rad(u1,u2,rad);
          #print(d1[0:100],d2[0:100]) #% correct for angle (clockw.)
          #print(np.max(np.abs(d1))**2,np.max(np.abs(d2))**2)
          SDavg[j] = np.sqrt(sum((np.max(np.abs(d1))**2,np.max(np.abs(d2))**2))/2); #% avg.peak of PC 
          #print('avg', SDavg[j])         
      
      PSVmax=SDmax*omega;
      PSAmax=SDmax*omega**2;
      PSVavg=SDavg*omega;
      PSAavg=SDavg*omega**2;
      
      
  
  ##% PGA
  PGAmax= np.max(np.sqrt(a1**2 + a2**2)); #% rotation invariant max
  #print('PGAmax',PGAmax)
  jia = solve(np.dot(np.transpose(a1),a1),np.dot(np.transpose(a1),a2))  
  rad = np.arctan(jia);
  #print(rad)   
  b1,b2 = Rot2CompCW_rad(a1,a2,rad);  
  PGAavg= np.sqrt(sum((np.max(np.abs(b1))**2,np.max(np.abs(b2))**2))/2); #% avg.peak of PC
  #print('PGAavg',PGAavg)

  #% PGV
  v1 = scipy.integrate.cumtrapz(tButterFilt(a1,dt,0.05,0,3), initial=0)*dt #% vel 1
  v2 = scipy.integrate.cumtrapz(tButterFilt(a2,dt,0.05,0,3), initial=0)*dt #% vel 2
  
  
  #v1 = cumtrapz(tButterFilt(a1,dt,0.05,0,3))*dt; 
  #v2 = cumtrapz(tButterFilt(a2,dt,0.05,0,3))*dt; % vel 2
  PGVmax= np.max(np.sqrt(v1**2 + v2**2)); #% rotation invariant max
  jiv = solve(np.dot(np.transpose(v1),v1),np.dot(np.transpose(v1),v2))
  rad = np.arctan(jiv);
    
  b1,b2 = Rot2CompCW_rad(v1,v2,rad);
  PGVavg= np.sqrt(sum((np.max(np.abs(b1))**2,np.max(np.abs(b2))**2))/2); #% avg.peak of PC
  
  Umax = pd.DataFrame()
  Umax['PGA_max'] = PGAmax*np.ones(len(periods))
  Umax['PGV_max'] = PGVmax*np.ones(len(periods))
  Umax['PSA_max'] = PSAmax
  Umax['PSV_max'] = PSVmax
  Umax['SD_max'] = SDmax
  Umax['PGA_avg'] = PGAavg*np.ones(len(periods))
  Umax['PGV_avg'] = PGVavg*np.ones(len(periods))
  Umax['PSA_avg'] = PSAavg
  Umax['PSV_avg'] = PSVavg
  Umax['SD_avg'] = SDavg  
  
  
  return Umax

  
  

  
