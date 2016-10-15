class TimeSeries:
    '''This is the TimeSeries class implemented using Python.
       The TimeSeries class can store a single, ordered set of numerical data.
    '''
    def __init__(self,data):
	'''The constructor should take the initial sequence-like data to fill the time series.
	'''
        self.timeSeries = data

    def __len__(self):
	'''Get the length of the timeseries data.
	'''
        return len(data)

    def __getitem__(self,index):
	'''Get the data at the position specified by index. 
	'''
        return data[index]
        
    def __setitem__(self,index,value):
        '''Set the data to the input value at the position specified by index.
	'''
	return data[index] = value

    def __str__(self):
