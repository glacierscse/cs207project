import sys
sys.path.append('../')

import os
import random
import pickle
from timeseries import ArrayTimeSeries
#from calculateDistance import calcDist, standardize
#from tsbtreedb import *
import click
import numpy as np
import json

def genMeta(sm):
	# number of ts data in ts_data/
	path = '../timeseries/timeseriesDB'
	num_ts = len(os.listdir(path))
	print(num_ts)

	for i in range(num_ts):
		#ts = pickle.load(open(path + '/ts_' + str(i) + '.dat', 'rb'))
		ts = sm.get(i)
		mean = ts.mean()
		std = ts.std()
		print(i,mean,std)

#if __name__ == '__main__':
#	genMeta()