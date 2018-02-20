import pandas as pd
from sklearn.linear_model import LogisticRegression
import pickle
import os, sys
sys.path.insert(0, os.path.abspath('.'))
sys.path.append('../')
from src import read_data, preprocess_for_sklearn

def fit_model(data):
    """
    Takes a tuple with X matrix and Y vector as input. Fits a logistic regression on them.
    Then pickles the model for future use.

    Args:
        data (tuple): Tuple with X matrix and Y vector for model fitting.
    """
    #prepare data
    X = preprocess_for_sklearn(data[0])
    y = data[1]
    #fit model
    logreg = LogisticRegression()
    logreg.fit(X, y)
    return logreg

def pickle_model(model):
    """
    Pickle the model
    """
    pkl_filename = '../models/logistic.pkl'
    model_pkl = open(pkl_filename, 'wb')
    pickle.dump(model, model_pkl)
    model_pkl.close()

if __name__ == "__main__":
    #fit_model_pickle(read_data())
    pickle_model(fit_model(read_data("employees_hist_data")))

