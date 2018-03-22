import os
import sys
sys.path.insert(0, os.path.abspath('.'))
sys.path.append('../')
sys.path.append('../../develop')
sys.path.append('../../develop/src')
import app.functions as f
import numpy

mylist = [0.2, .8, 3, 280, 4, 0, 0, 14, 16]
data = f.preprocess_prediction_form_data(mylist)

def test_preptable_type():
    """Check preprocess_prediction_form_data returns a numpy.ndarray."""
    assert isinstance(data, numpy.ndarray)


def test_preprocess_length():
    """Check preprocess_prediction_form_data returns an array with
    18 elements."""
    assert len(data[0]) == 18

def test_preprocess_dept():
    """Check preprocess_prediction_form_data deals correctly with data
    regarding the department an employee works in."""
    assert list(data[0])[13:16] == [0,1,0]


def test_preprocess_salary():
    """Check preprocess_prediction_form_data deals correctly with data
    regarding the salary of an employee."""
    assert list(data[0])[16:18] == [1,0]


def test_give_promotion():
    """Check give_promotion correctly changes the salary category
    dummies and the got_a_promotion binary."""
    promotion = list(f.give_promotion(data)[0])
    assert (promotion[16:18] == [0,1]) & (promotion[6] == 1)


def test_increase_satisfaction():
    """Check increase_satisfaction correctly increases the
    satisfaction of the employee."""
    assert round(f.increase_satisfaction(data)[0][0], 2) == 0.3


def test_reduce_workload():
    """Check increase_satisfaction correctly reduces the
    workload of the employee."""
    assert f.reduce_workload(data)[0][3] == 280*0.9
