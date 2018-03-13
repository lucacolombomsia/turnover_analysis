import os
import sys
sys.path.insert(0, os.path.abspath('.'))
sys.path.append('../')
sys.path.append('../src')
from src import preprocess_for_sklearn
import src.makedb
import src.model
import pytest
import pandas as pd
import yaml
import numpy as np
import sklearn


# read in the yaml file
with open('../../params.yaml', 'r') as f:
    model_meta = yaml.load(f)
path = model_meta['directories']['train_data'].replace('develop', '..')
path2 = model_meta['directories']['names'].replace('develop', '..')


# call db.prep_tables function once and assing to object
# will use this object for testing
prep_table = src.makedb.prep_tables(path, path2, 
                                    model_meta['test_size'],
                                    model_meta['random'])


def test_preptable_type():
    """Check prep_tables returns a tuple."""
    assert isinstance(prep_table, tuple)


def test_preptable_length():
    """Check prep_tables returns a tuple with 3 elements."""
    assert len(prep_table) == 3


def test_preptable_size():
    """
    Check test set tables have the desired shape.
    The number of rows should be the test_size set in the yaml file.
    There should be 11 columns.
    """
    assert prep_table[1].shape == (int(model_meta['test_size']/2), 11)


# read in the data from csv (so that we do not have to depend on database)
# this will ensure we can test functions even if db connection does
# not work
# data must be right input, ie the input that is usually fed to
# the preprocess_for_sklearn function
data = prep_table[1]


def test_preprocess_type():
    """Check preprocess_for_sklearn returns a pandas dataframe."""
    assert isinstance(preprocess_for_sklearn(data), pd.DataFrame)


def test_preprocess_size():
    """Check preprocess_for_sklearn returns df with the right number of columns."""
    assert preprocess_for_sklearn(data).shape[1] == 18


def test_preprocess_allnumeric():
    """Check preprocess_for_sklearn returns df with only numeric columns."""
    is_number = np.vectorize(lambda x: np.issubdtype(x, np.number))
    assert (sum(is_number(preprocess_for_sklearn(data).dtypes)) == 
            preprocess_for_sklearn(data).shape[1])


# fit a logistic regression model on the training data
# will store the fitted model in an object that we can use for testing
# also, read test_data
training_data = prep_table[0]
model = src.model.fit_model(training_data)
test_data = np.array([preprocess_for_sklearn(prep_table[1]).loc[0,:]])

def test_model_type():
    """Check fit_model returns a sklearn Logistic Regression model."""
    assert isinstance(model, sklearn.linear_model.LogisticRegression)

def test_model_prediction():
    """
    Check that output of fit_model can be used to make predictions.
    It is a logistic regression model, hence the predicted probability
    should be between 0 and 1.
    """
    pred = model.predict_proba(test_data)[0][1]
    assert ((pred>0) & (pred<1))
