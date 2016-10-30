from pytest import raises
from TimeSeries import TimeSeries
from TimeSeries import ArrayTimeSeries

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

#-------setitem test cases----------
# norm case
def test_setitem():
    data = [4, 5, 6]
    time = [1, 2, 3]
    ts = TimeSeries(data, time)
    index = 0
    val = 0
    ts[index] = val
    assert ts == TimeSeries([0, 5, 6],[1, 2, 3])

# index out of range
def test_setitem_index_error():
    data = [4, 5, 6]
    time = [1, 2, 3]
    ts = TimeSeries(data, time)
    index = 5
    val = 0
    with raises(IndexError):
        ts[index] = val

#--------repr test cases---------
# length less or equal than five 
def test_repr_less_than_five():
    data = [4, 5, 6]
    time = [1, 2, 3]
    ts = TimeSeries(data, time)
    assert repr(ts) == 'TimeSeries([(1, 4), (2, 5), (3, 6)])'

# length greater than five
def test_repr_greater_than_five():
    data = [4, 5, 6, 7, 8, 9]
    time = [1, 2, 3, 4, 5, 6]
    ts = TimeSeries(data, time)
    assert repr(ts) == 'TimeSeries([(1, 4), (2, 5), (3, 6), (4, 7), (5, 8), (6, 9)])'

#--------str test cases-----------
# length less or equal than five 
def test_str_less_than_five():
    data = [4, 5, 6]
    time = [1, 2, 3]
    ts = TimeSeries(data, time)
    assert str(ts) == '[(1, 4), (2, 5), (3, 6)]'

# length greater than five
def test_str_greater_than_five():
    data = [4, 5, 6, 7, 8, 9]
    time = [1, 2, 3, 4, 5, 6]
    ts = TimeSeries(data, time)
    assert str(ts) == '[(1, 4), (2, 5), (3, 6), (4, 7), (5, 8) ... (6, 9)]'

#--------eq test cases--------
# correct cases
def test_eq_correct():
    ts1 = TimeSeries([4, 5, 6], [1, 2, 3])
    ts2 = TimeSeries([4, 5, 6], [1, 2, 3])
    assert (ts1 == ts2) == True

# different types
def test_eq_diff_type():
    ts1 = TimeSeries([4, 5, 6], [1, 2, 3])
    ts2 = 3
    assert (ts1 == ts2) ==  False

# different length
def test_eq_diff_len():
    ts1 = TimeSeries([4, 5, 6], [1, 2, 3])
    ts2 = TimeSeries([4, 5], [1, 2])
    assert (ts1 == ts2) == False

# different value
def test_eq_diff_value():
    ts1 = TimeSeries([4, 5, 6], [1, 2, 3])
    ts2 = TimeSeries([4, 5, 7], [1, 2, 3])
    assert (ts1 == ts2) == False

# different key
def test_eq_diff_time():
    ts1 = TimeSeries([4, 5, 6], [1, 2, 3])
    ts2 = TimeSeries([4, 5, 6], [1, 2, 4])
    assert (ts1 == ts2) == False
 
#-------ArrayTimeSeries constructor test cases----------
#test no input argument
def test_init_no_argument():
    with raises(TypeError):
        ArrayTimeSeries()

#test one input argument
def test_init_argument():
    data = [1, 2, 3]
    with raises(TypeError):
        ArrayTimeSeries(data)

#test multiple arguments
def test_two_arguments():
    data = [1, 2, 3]
    time = [4, 5, 6]
    ArrayTimeSeries(time, data)

#test the length of the input argument is zero
def test_init_zero_length_argument():
    data = []
    time = []
    ArrayTimeSeries(time, data)
    
#test different length arguments
def test_init_diff_length_argument():
    data = []
    time = [1,2,3]
    with raises(Exception):
        ArrayTimeSeries(time, data)


    #your constructor, which should take one mandatory argument which represents 
    #data to fill the time series instance with. 
    #This argument should be any object that can be treated like a sequence. 
    #The argument can be zero-length, but it can't be omitted.	

#if __name__ == '__main__':
#    unittest.main()
