import numbers, reprlib
class TimeSeries:
    # TimeSeries class	
    def __init__(self,data):
        self._time_series = data
    # get the length of data
    def __len__(self):
        return len(self._time_series)

    def __getitem__(self,index):
        cls = type(self)
        if isinstance(index, slice):
            return cls(self._time_series[index])
        elif isinstance(index, numbers.Integral): 
            return self._time_series[index]
        
    def __setitem__(self,index,value):
        self._time_series[index] = value

