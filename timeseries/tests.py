from pytest import raises
from TimeSeries import TimeSeries
#import unittest

#class TestTimeSeries(unittest.TestCase):

#-------constructor test cases----------
#test no input argument 
def test_init_no_argument():
    with raises(TypeError):
        TimeSeries()
        #time_series_test = TimeSeries()

#test one input argument 
def test_init_argument():
    input = [1,2,3]
    TimeSeries(input)

#test multiple arguments
def test_two_arguments():
    a = [1,2,3]
    b = [-15,4.5,12] #increasing values?
    TimeSeries(a,b)

#test the length of the input argument is zero
def test_init_zero_length_argument():
    input = []
    TimeSeries(input)

#test different length arguments
def test_init_diff_length_argument():
    a = []
    b = [1,2,3]
    with raises(Exception):
        TimeSeries(a,b)

#-------len test cases----------
def test_length():
    a = [1,2,3]
    ts = TimeSeries(a)
    assert len(ts) == 3

def test_zero_length():
    a = []
    ts = TimeSeries(a)
    assert len(ts) == 0

#-------getitem test cases----------


    #your constructor, which should take one mandatory argument which represents 
    #data to fill the time series instance with. 
    #This argument should be any object that can be treated like a sequence. 
    #The argument can be zero-length, but it can't be omitted.	

#if __name__ == '__main__':
#    unittest.main()
