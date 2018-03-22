import pytest
import pandas as pd
import yaml
import numpy as np
import sklearn
import os
import sys
sys.path.insert(0, os.path.abspath('.'))
sys.path.append('../')
sys.path.append('../src')
from src import preprocess_for_sklearn
import src.makedb
import src.model


def read_yaml():
    # function for reading the yaml file
    with open('../../params.yaml', 'r') as f:
        model_meta = yaml.load(f)
    return model_meta


def prep_table():
    # function that calls prep_tables
    # need to read the yaml file and modify two paths
    model_meta = read_yaml()
    path = model_meta['directories']['train_data'].replace('develop', '..')
    path2 = model_meta['directories']['names'].replace('develop', '..')
    # call the function that we want to test so that we don't have to specify
    # all the arguments in each test
    table = src.makedb.prep_tables(path, path2,
                                   model_meta['test_size'],
                                   model_meta['random'])
    return table


def test_preptable_type():
    """Check prep_tables returns a tuple."""
    assert isinstance(prep_table(), tuple)


def test_preptable_length():
    """Check prep_tables returns an object of length 3."""
    assert len(prep_table()) == 3


def test_preptable_size():
    """
    Check that the test set tables have the desired shape.
    The number of rows should be the test_size set in the yaml file.
    There should be 11 columns.
    """
    model_meta = read_yaml()
    tables = prep_table()
    assert tables[1].shape == (int(model_meta['test_size']/2), 11)


def test_preprocess_type():
    """Check preprocess_for_sklearn returns a pandas dataframe."""
    # we must have the right input, ie the input that is usually fed to
    # the preprocess_for_sklearn function
    data = prep_table()[1]
    assert isinstance(preprocess_for_sklearn(data), pd.DataFrame)


def test_preprocess_size():
    """Check preprocess_for_sklearn returns a dataframe with the right
    number of columns."""
    # we must have the right input, ie the input that is usually fed to
    # the preprocess_for_sklearn function
    data = prep_table()[1]
    assert preprocess_for_sklearn(data).shape[1] == 18


def test_preprocess_allnumeric():
    """Check preprocess_for_sklearn returns df with only numeric columns."""
    # we must have the right input, ie the input that is usually fed to
    # the preprocess_for_sklearn function
    data = prep_table()[1]
    is_number = np.vectorize(lambda x: np.issubdtype(x, np.number))
    assert (sum(is_number(preprocess_for_sklearn(data).dtypes)) ==
            preprocess_for_sklearn(data).shape[1])


def fit_model():
    # function that calls the src.model.fit_model function
    # we are fitting a random forest on the training data
    # the tuning parameters come from the yaml file
    # the function return the model that can be used for testing
    model_meta = read_yaml()
    training_data = prep_table()[0]
    model = src.model.fit_model(training_data,
                                depth=model_meta['model']['max_depth'],
                                seed=model_meta['model']['seed'],
                                ntrees=model_meta['model']['ntrees'])
    return model


def read_test_data():
    # function for reading one line from the test set into the right format
    # the data will be used to check that model can be used for prediction
    # need a 2D numpy array with the first row of the preprocessed for sklean
    test_data = prep_table()[1]
    return np.array([preprocess_for_sklearn(test_data).loc[0, :]])


def test_model_type():
    """Check fit_model returns a sklearn Random Forest Classifier model."""
    model = fit_model()
    assert isinstance(model, sklearn.ensemble.forest.RandomForestClassifier)


def test_model_prediction():
    """
    Check that output of fit_model can be used to make predictions.
    It is a random forest classifier, hence it should return a predicted
    probability between 0 and 1.
    """
    model = fit_model()
    test_data = read_test_data()
    pred = model.predict_proba(test_data)[0][1]
    assert ((pred > 0) & (pred < 1))
