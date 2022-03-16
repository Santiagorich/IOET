import json
import datetime
import pytest
from utils import *

#Test Deserialize
def test_app1():
    result = deserialize_schedules('RENE=MO10:00-12:00,TU10:00-12:00,TH01:00-03:00,SA14:00-18:00,SU20:00-21:00')
    assert result[0]['pay'] == 215

#Test Deserialize Half an hour
def test_app2():
    result = deserialize_schedules('PASCUALINA=MO10:00-11:30,SA14:30-18:00,SU20:30-21:00')
    assert result[0]['pay'] == 105


#Invalid Input
@pytest.mark.xfail(raises=Exception)
def test_app3():
    assert deserialize_schedules('RENE=MO10:00-12:0wwwwwwww')
    
#Check should throw an error if the start hour comes after the end hour
@pytest.mark.xfail(raises=ValueError)
def test_app4():
    assert check_shift({'day': 'MO', 'start': datetime(1900, 1, 1, 13, 0), 'end': datetime(1900, 1, 1, 12, 0)},'RENE')

def test_app5():
    result = calculate_pay({'day': 'MO', 'start': datetime(1900, 1, 1, 10, 0), 'end': datetime(1900, 1, 1, 12, 0)})
    assert result == 30
    
