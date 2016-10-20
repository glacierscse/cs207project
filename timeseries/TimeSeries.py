import numbers
from reprlib import recursive_repr
import numpy as np
class TimeSeries:
    '''This is the TimeSeries class implemented using Python.
       The TimeSeries class can store a single, ordered set of numerical data.
    '''
    def __init__(self, data, time = None):
        '''The constructor should take the initial sequence-like data to fill the time series.
           The sequence-like data can have length 0, but must be given.
        '''
        len_data = len(data)
        if time == None:
            self._key = list(range(len_data))
        else:
            self._key = time
        self._value = data
        self._time_series = list(zip(self._key, self._value))
    
    def __len__(self):
        '''Get the length of the timeseries data.
        '''
        return len(self._value)

    def __getitem__(self,index):
        '''Get the data at the position specified by index. 
        '''
        cls = type(self)
        if isinstance(index, slice):
            return cls(self._time_series[index])
        elif isinstance(index, numbers.Integral):
            return self._time_series[index]
    
    def __setitem__(self, index, pair):
        '''Set the data to the input value at the position specified by index.
        '''
        self._time_series[index] = pair

    @recursive_repr()
    def __repr__(self):
        '''Return formal string representation of the timeseries data.
        '''
        class_name = type(self).__name__
        return class_name + '(' + ', '.join(map(repr, self)) + ')'
        
    def __str__(self):
        limit_len = 5
        len_data = len(self._time_series)
        if len_data <= limit_len:
            return str(self._time_series)
        else:
            str_part1 = ", ".join(str(item) for item in self._time_series[0:limit_len])
            return "[" + str_part1 + " ... " + str(self._time_series[-1]) + "]" 

    def __iter__(self):
        for val in self._value:
            yield val

    def itervalues(self):
        for val in self._value:
            yield val

    def itertimes(self):
        for time in self._key:
            yield time

    def iteritems(self):
        for item in self._time_series:
            yield item

    #def values(self):
     #   return np.array(self._value)



