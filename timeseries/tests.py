import unittest
from TimeSeries import TimeSeries


class TestTimeSeries(unittest.TestCase):

    #test no input argument for constructor
    def test_init_no_argument(self):
        with self.assertRaises(TypeError):
            time_series_test = TimeSeries()

    #test multiple arguments for constructor 
    def test_init_multiple_arguments(self):
        a = [1]
        b = [2]
        with self.assertRaises(TypeError):
            time_series_test = TimeSeries(a,b)

    #test the input argument for constructor is zero-length
    def test_init_zero_length_argument(self):
        input = []
        TimeSeries(input)

    def test_init_argument(self):
        input = [1]
        TimeSeries(input)

    #def test_
    #your constructor, which should take one mandatory argument which represents 
    #data to fill the time series instance with. 
    #This argument should be any object that can be treated like a sequence. 
    #The argument can be zero-length, but it can't be omitted.	

if __name__ == '__main__':
    unittest.main()
