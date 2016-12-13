from error import *
from collections import OrderedDict
import sys
sys.path.append('../')
from timeseries.TimeSeries import TimeSeries

# Interface classes for TSDB network operations.
# These are a little clunky (extensibility is meh), but it does provide strong
# typing for TSDB ops and a straightforward mechanism for conversion to/from
# JSON objects.


class TSDBOp(dict):
    def __init__(self, op):
        self['op'] = op

    def to_json(self, obj=None):
        if obj is None:
            obj = self
        json_dict = {}
        if isinstance(obj, str) or not hasattr(obj, '__len__') or obj is None:
            return obj
        for k, v in obj.items():
            if isinstance(v, str) or not hasattr(v, '__len__') or v is None:
                json_dict[k] = v
            elif isinstance(v, TSDBStatus):
                json_dict[k] = v.name
            elif isinstance(v, list):
                json_dict[k] = [self.to_json(i) for i in v]
            elif isinstance(v, OrderedDict):    ####### this one seems to be unnecessary. Myra
                tuples=[]
                for key in v:
                    tuples.append((key, self.to_json(v[key])))
                json_dict[k] = OrderedDict(tuples)
            elif isinstance(v, dict):
                json_dict[k] = self.to_json(v)
            elif hasattr(v, 'to_json'):
                json_dict[k] = v.to_json()
            else:
                raise TypeError('Cannot convert object to JSON: '+str(v))
        return json_dict

    @classmethod
    def from_json(cls, json_dict):
        if 'op' not in json_dict:
            raise TypeError('Not a TSDB Operation: '+str(json_dict))
        if json_dict['op'] not in typemap:
            raise TypeError('Invalid TSDB Operation: '+str(json_dict['op']))
        return typemap[json_dict['op']].from_json(json_dict)


class TSDBOp_Return(TSDBOp):

    def __init__(self, status, op, payload=None):
        super().__init__(op)
        self['status'], self['payload'] = status, payload

    @classmethod
    def from_json(cls, json_dict):
        return cls(json_dict['status'], json_dict['payload'])

# Myra
class TSDBOp_Simquery_WithID(TSDBOp):
    def __init__(self, idee):       ######**kwargs
        super().__init__('simquery_id')
        self['id'] = idee

    @classmethod
    def from_json(cls, json_dict):
        return cls(json_dict['id'], n=json_dict['n'])

#Myra
class TSDBOp_Simquery_WithTS(TSDBOp):
    def __init__(self, ts):
        super().__init__('simquery_ts')
        self['ts'] = ts

    @classmethod
    def from_json(cls, json_dict):
        return cls(ts.TimeSeries(*(json_dict['ts'])), n=json_dict['n'])


#Myra
class TSDBOp_GetTS_WithID(TSDBOp):
    def __init__(self, idee):
        super().__init__('get_id')
        self['id'] = idee

    @classmethod
    def from_json(cls, json_dict):
        return cls(json_dict['id'])




# This simplifies reconstructing TSDBOp instances from network data.
typemap = {
    'simquery_ts': TSDBOp_Simquery_WithTS,
    'simquery_id': TSDBOp_Simquery_WithID,
    'get_id': TSDBOp_GetTS_WithID
}