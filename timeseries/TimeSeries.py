import numbers, reprlib
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
        return len(self._time_series)

    def __getitem__(self,index):
	'''Get the data at the position specified by index. 
	'''
        cls = type(self)
        if isinstance(index, slice):
            return cls(self._time_series[index])
        elif isinstance(index, numbers.Integral):
            return self._time_series[index]
    
    def __setitem__(self,index,value):
        '''Set the data to the input value at the position specified by index.
	'''
        self._time_series[index] = value

