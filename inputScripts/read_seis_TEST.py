#!/usr/bin/env python

import sys
import os
import struct
import matplotlib.pyplot as plt
import numpy as np

'''struct seisheader {
  char version[8];
  char site_name[8];
  //in case we think of something later
  char padding[8];
  int source_id;
  int rupture_id;
  int rup_var_id;
  float dt;
  int nt;
  int comps;
  float det_max_freq;
  float stoch_max_freq;
  };'''

class Seismogram:	
	def __init__(self, filename):
		self.filename = filename
		self.nt = 0
		self.dt = 0.0
		self.data_dict = dict()
		self.rvs = []
	def createTimesteps(self):
		self.timesteps = []
		for i in range(0, self.nt):
			self.timesteps.append(i*self.dt)
	def parseHeader(self, header_str):
		#rv is 32-36, dt is bytes 36-40, nt is 40-44
		rv = struct.unpack('i', header_str[32:36])[0]
		self.dt = struct.unpack("f", header_str[36:40])[0]
		self.nt = struct.unpack("i", header_str[40:44])[0]
		return rv
	def readData(self):
		fp_in = open(self.filename, "rb")
		header_str = fp_in.read(56)
		self.parseHeader(header_str)
		filesize = os.path.getsize(self.filename)
		self.num_rvs = filesize//(56 + 2*self.nt*4)
		if (56+2*self.nt*4)*self.num_rvs!=filesize:
		        #print("Mismatch between filesize of %d and %d variations with %d bytes each, aborting." % (filesize, self.num_rvs, (56+2*self.nt*4)))
		        sys.exit(1)
		#Reset fp
		fp_in.seek(0)
		for i in range(0, self.num_rvs):
			header_str = fp_in.read(56)
			rv = self.parseHeader(header_str)
			self.rvs.append(rv)
			data_str = fp_in.read(4*self.nt)
			x_data = struct.unpack("%df" % self.nt, data_str)
			data_str = fp_in.read(4*self.nt)
			y_data = struct.unpack("%df" % self.nt, data_str)
			self.data_dict[rv] = (x_data, y_data)
		fp_in.close()


#if len(sys.argv)<2:
	#print("Usage: %s <grm file>" % (sys.argv[0]))
	#sys.exit(1)

#grm_file = 'Seismogram_SS_570_1_988_52.grm' # sys.argv[1]

#seis = Seismogram(grm_file)
#seis.readData()
###Data for rupture variation RV is stored in seis.data_dict[RV]
##for i in range(0, seis.num_rvs):
  
#i = 0
#rv_id = seis.rvs[i]
#nt = seis.nt
#dt = seis.dt
#time = seis.dt*np.arange(0.5,seis.nt-0.5,1) 
#(x_data, y_data) = seis.data_dict[i]
#x_data = np.asarray(x_data)
#y_data = np.asarray(y_data)
#Ax = (1/dt)*(x_data[1:nt] - x_data[0:nt-1]); Ay = (1/dt)*(y_data[1:nt] - y_data[0:nt-1]);

#plt.figure(1)
#plt.plot(time, Ax, 'b')
#plt.plot(time, Ay, 'r')
#plt.show()



