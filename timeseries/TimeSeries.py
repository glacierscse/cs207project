class TimeSeries:
    def __init__(self,data):
        self.timeSeries = data

    def __len__(self):
        return len(data)

    def __getitem__(self,index):
        return data[index]
        
    def __setitem__(self,index,value):
        return data[index] = value
