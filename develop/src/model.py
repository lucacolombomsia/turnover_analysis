from sklearn.linear_model import LogisticRegression
import pickle
import logging
import argparse
import yaml
import os
import sys
sys.path.insert(0, os.path.abspath('.'))
sys.path.append('develop/')
from src import read_data, preprocess_for_sklearn


def fit_model(data):
    """Fit a logistic regression on the training data.

    The input should be the training data read from the database.
    The output of this function should be fed to the pickle_model function
    so that the model can be pickled and stored for future use.

    Args:
        data (pd.DataFrame): The training data read from database.

    Returns:
        A trained logistic regression model
    """
    # get logger
    logger = logging.getLogger(__name__)

    # notice that data contains both response and predictors
    # X matrix is all columns but "left", the response
    X = preprocess_for_sklearn(data.drop(["left"], axis=1))
    y = data.left
    logger.info('Data has been preprocessed for sklearn')
    # fit model
    logreg = LogisticRegression()
    logreg.fit(X, y)
    logger.info('Model has been fit')
    return logreg


def pickle_model(model):
    """Take a trained model and write it into a pickle file.

    Args:
        model: A trained model.
    """
    # get logger
    logger = logging.getLogger(__name__)

    model_pkl = open(model_meta['directories']['pkl'], 'wb')
    pickle.dump(model, model_pkl)
    model_pkl.close()
    logger.info('Model has been pickled and stored')


if __name__ == "__main__":
    # handle command line arguments (location of yaml file)
    parser = argparse.ArgumentParser()
    parser.add_argument('meta_path', help="path of the yaml file")
    args = parser.parse_args()
    # read in the yaml file
    with open(args.meta_path, 'r') as f:
        model_meta = yaml.load(f)

    # setup log file
    log_fmt = '%(asctime)s - %(levelname)s - %(message)s'
    logging.basicConfig(filename=model_meta['directories']['log'],
                        level=logging.INFO, format=log_fmt)
    logger = logging.getLogger(__name__)

    pickle_model(fit_model(read_data("employees_hist_data")))
