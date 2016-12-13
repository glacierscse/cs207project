from timeseries.FileStorageManager import FileStorageManager
from p7_simsearch.genTS import genTS
from API.genMeta import genMeta

if __name__ == '__main__':
	#For RBDB
	n_generate = 1000
	s = FileStorageManager("timeseries/timeseriesDB")
	#generate RBDB and SMDB
	genTS(n_generate, s)

	#generate metaDB
	genMeta(s)



