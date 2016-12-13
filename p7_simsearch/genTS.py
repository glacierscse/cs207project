import sys
sys.path.append('../')
from timeseries.SMTimeSeries import SMTimeSeries

import os
import pickle
import random

from calculateDistance import tsmaker, standardize
import click

m_a, m_b = -100, 100
s_a, s_b = 0.1, 10
j_a, j_b = 1, 50

@click.command()
@click.option('-n', default=1000, help='number of ts to generate, default 1000')
@click.option('--n', default=1000, help='number of ts to generate, default 1000')
def genTS(n, sm):
	"""generate n standardized time series, each stored in a file in ts_data/.
	"""
	if not os.path.exists('ts_data/'):
		os.makedirs('ts_data/')

	m = [random.uniform(m_a, m_b) for i in range(n)]
	s = [random.uniform(s_a, s_b) for i in range(n)]
	j = [random.randint(j_a, j_b) for i in range(n)]

	for i in range(n):
		with open('ts_data/ts_' + str(i) + '.dat', 'wb+') as f:
			ts = standardize(tsmaker(m[i], s[i], j[i]))
			pickle.dump(ts, f)

	for i in range(n):
		ts = tsmaker(m[i], s[i], j[i])
		smts = SMTimeSeries(ts.times(), ts.values(), sm)

#if __name__ == '__main__':
#	genTS()