import numpy as np
def Rot2CompCW_rad(a1,a2,rad):

#%Script to Python Marisol Monterrubio 13/2/2023
#% Take 2 (horizontal) timeseries components and rotate both clockwise about
#% the same angle 'rad' [input in radian].
#%
#% 2019-02-09 tsonne, 
#%   based on my function .../PhD/M/Mai/class_project/Rot_2Comp_Clockw.m
#%
#% when assuming North and East components, deg = strike angle ...
  FI=[ np.cos(rad),  np.sin(rad),  -np.sin(rad),  np.cos(rad)];  #% Note: N'=FI*N. Rotation of N #% clockwise about angle fi, gives N'
  print(FI, FI[0])
  # then we get ...
  ra1 = FI[0]*a1 + FI[1]*a2; #% Strike parallel component
  ra2 = FI[2]*a1 + FI[3]*a2; #% Strike perpendicular (clockwise)
  return ra1,ra2
