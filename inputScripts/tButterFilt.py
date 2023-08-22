import numpy as np
from scipy.signal import lfilter, lfiltic,filtfilt, butter


def tButterFilt(a,dt,f_lo,f_hi,order):
#%Script to Python Marisol Monterrubio 13/2/2023
#% Low|High|Bandpass filter all timeseries in cell array:
#% use Butterworth filter on a cell array 'a' with rows for stations
#% and columns for components, where 'dt' is a vector of length size(a,1)
#% which contains the sampling interval dt for each station.
#% 'a' and 'dt' can also be input as vector with scalar,
#% 'a' can also be a matrix with each column taken as time series and one
#% common 'dt' or matching vector 'dt'.
#%
#% INPUT:
#%   a = vector, matrix or cell(r,c) of time series amplitudes
#%   dt = scalar or vector (length=r, one dt value for each station in a)
#%   f_lo = low  corner frequency (set 0 if Lowpass wanted)
#%   f_hi = high corner frequency (set 0 if Highpass wanted)
#% optional:
#%   order = order of Butterworth filter (single pass) (DEFAULT: 3)
#%           Will be double in effect when filtfilt used (back-forth pass)
#%   causal = say 'causal','y','yes' or 1 if only one pass requested
#%
#% OUTPUT:
#%   afilt = vector, matrix or cell(r,c), filter applied to all time series
#% 
#% 2016-03-22 tsonne
#% 2016-04-22 tsonne: added matrix input for 'a'.

  causal=0

  #if iscell(a)
  a = np.asarray(a)    
  #print(a.ndim)
  nr = len(a);
  nc = 1
  #print('nr',nr,'nc',nc)
  afilt = np.zeros(nr);
  if np.size(dt)==1:
      dt = dt*np.ones((nr,1));
  if np.size(dt)==nr:
    
    afilt = tButterworth(a,dt,f_lo,f_hi,order,causal);
    #print('afilt', afilt[0:30])
    
     
  #else
      #[nr nc] = size(a);
      #afilt = nan(nr,nc);
      #if numel(dt)==1
          #dt = dt*ones(1,nc);
      #end
      #assert(length(dt)==nc,'Given dt and number of time series mismatch!')
      #for j = 1:nc
          #afilt(:,j) = tButterworth(a(:,j),dt(j),f_lo,f_hi,order,causal);
      #end
      
  #end
 
  return afilt

#% SUBROUTINE: BUTTERWORTH FILTER

def tButterworth(a,dt,f_lo,f_hi,order,causal):
  fny = 0.5/dt;
  if f_lo == 0:
      ftyp = 'lowpass'
      fbp = f_hi/fny
  elif f_hi == 0:
      ftyp = 'highpass';
      fbp = f_lo/fny;  
  #print('fbp',fbp)
  #print('ftyp', ftyp)
  #print('order',order)
  z,p = butter(order, fbp[0], ftyp);
  #print('z',z,'p',p)
  afilt = filtfilt(z,p,a);
    
  return afilt 
