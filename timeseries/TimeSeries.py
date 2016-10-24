import numbers
import reprlib
import numpy as np
import sys
from lazy import LazyOperation

class TimeSeries:
    '''This is the TimeSeries class implemented using Python.
       The TimeSeries class can store time series data.
    '''
    def __init__(self, data, time = None):
        '''The constructor should take the initial sequence-like data to fill the time series.
           The sequence-like data can have length 0, but must be given.
           Time is an optional argument.
        '''
        ##the time has to be in order when pass in -- precondtion
        len_data = len(data)
        if time == None:
            self._key = list(range(len_data))
        else:
            self._key = time
        self._value = data
        if len(self._value) != len(self._key):
            raise Exception('The length of time input has to be equal to the length of value input')
        #self._time_series = list(zip(self._key, self._value))
  
    def __len__(self):
        '''Get the length of the timeseries data.
        '''
        return len(self._value)

    def __getitem__(self,index):
        '''Get the data at the position specified by index. 
        '''
        cls = type(self)
        if isinstance(index, slice):
            return cls(self._value[index],self._key[index])
        elif isinstance(index, numbers.Integral):
            return (self._key[index],self._value[index])
    
    def __setitem__(self, index, val):
        '''Set the data to the input value at the position specified by index.
        '''
        #pass in only the value. We can't change the time -- precondition
        self._value[index] = val

 
    #@recursive_repr()
    #not complete
    #def __repr__(self):
    #    '''Return formal string representation of the timeseries data.
    #    '''
    #    class_name = type(self).__name__
    #    return class_name + '(' + ', '.join(map(repr, self)) + ')'
    def __repr__(self):
        '''Return formal string representation of the timeseries data.
        '''
        time_series = list(zip(self._key, self._value))
        components = reprlib.repr(time_series)
        components = components[components.find('['):]
        return 'TimeSeries({})'.format(components)

    def __str__(self):
        '''Return a string representation of the timeseries data.
           If the data length exceed the length limit, 
           the function will present part of the time series.
        '''
        limit_len = 5
        len_data = len(self._value)
        time_series = list(zip(self._key,self._value))
        if len_data <= limit_len:
            str_part1 = ", ".join(str(item) for item in time_series)
            return "[" + str_part1 + "]" 
            #return str(self._time_series)
        else:
            str_part1 = ", ".join(str(item) for item in time_series[0:limit_len])
            return "[" + str_part1 + " ... " + str(time_series[-1]) + "]" 

    def __iter__(self):
        '''Iterates over time series values.
        '''
        for val in self._value:
            yield val

    def itervalues(self):
        '''Returns an iterator over the time series values.
        '''
        for val in self._value:
            yield val

    def itertimes(self):
        '''Return an iterator over the time series times.
        '''
        for time in self._key:
            yield time

    def iteritems(self):
        '''Return an iterator over the time series time-value tuple pairs.
        '''
        time_series = zip(self._key, self._value)
        for item in time_series:
            yield item

    def values(self):
        '''Returns a numpy array of values.
        '''
        return self._value

    def times(self):
        '''returns a numpy array of times.
        '''
        return self._key

    def items(self):
        '''Return a list of time-value tuple pairs.
        '''
        return list(zip(self._key, self._value))

    def __contains__(self,val):
        return val in self._value


    def interpolate(self, inter_time):
        inter_values = []
        for ti in inter_time:
            if ti < self._key[0]:
                inter_values.append(self._value[0])
            
            elif ti > self._key[-1]:
                inter_values.append(self._value[-1])
            
            else:
                left, right = self._binary_search(self._key, ti)
                if left == right:
                    inter_values.append(self._value[left])
                else:
                    slope = (self._value[right] - self._value[left]) / (self._key[right]- self._key[left])
                    pred_value = (ti- self._key[left])*slope + self._value[left]
                    inter_values.append(pred_value)

        result = TimeSeries(inter_values, inter_time)
        return result

    def _binary_search(self, arr, target):
        if len(arr) == 0: 
            return -1 
        lo = 0
        hi = len(arr)-1
        while lo <= hi: 
            mid = lo+(hi-lo)//2
            if target < arr[mid]:
                hi = mid - 1
            elif target > arr[mid]:
                lo = mid + 1
            else: 
                return mid, mid
        return hi, lo


    def __eq__(self, other):
        if type(self) != type(other):
            return False
        if len(self) != len(other):
            return False
        if self._value == other._value and self._key == other._key:
            return True
        else:
            return False

    @property
    def lazy(self):
        identity = lambda x: x
        return LazyOperation(identity, self)


class ArrayTimeSeries(TimeSeries):
    def __init__(self, time, data):
        if len(time) != len(data):
            raise Exception('The length of time input has to be equal to the length of value input')
        self._key = np.array(time)
        self._value = np.array(data)
        #self._time_series = np.array(list(zip(time, data)))

    #def __len__(self):
    #    return self._value.shape[0]


    #def __getitem__(self, index):
    


    #def __setitem__(self, index, pair):


