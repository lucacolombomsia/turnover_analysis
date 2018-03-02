import pandas as pd
from sklearn.linear_model import LogisticRegression
import pickle
import os, sys
sys.path.insert(0, os.path.abspath('.'))
sys.path.append('develop/')
from src import read_data, preprocess_for_sklearn

def fit_model(data):
    """Fits a logistic regression on the training data that has been read from the database.

    Args:
        data (tuple): Tuple with X matrix and Y vector.

    Returns:
        A trained logistic regression model
    """
    #prepare data
    X = preprocess_for_sklearn(data[0])
    y = data[1]
    #fit model
    logreg = LogisticRegression()
    logreg.fit(X, y)
    return logreg

def pickle_model(model):
    """Takes a trained model and writes it into a pickle file.

    Args:
        model: A trained model.
    """
    pkl_filename = 'develop/models/logistic.pkl'
    model_pkl = open(pkl_filename, 'wb')
    pickle.dump(model, model_pkl)
    model_pkl.close()

if __name__ == "__main__":
    pickle_model(fit_model(read_data("employees_hist_data")))

