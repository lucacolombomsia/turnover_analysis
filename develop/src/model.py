import config
import pandas as pd
from sqlalchemy import create_engine
from sklearn.linear_model import LogisticRegression
import pickle

def read_data():
    """
    Reads the data from the employees table in the DB. Preprocesses data for model fitting.
    Returns a tuple with the X matrix and Y vector (in that order).

    Returns:
        tuple: A tuple with the X matrix and the Y vector.
    """
    engine = create_engine(config.database_config)
    emp = pd.read_sql_query("select * from employees", con = engine)
    y = emp['left']
    emp = emp.drop('left', axis=1)
    emp.sales = emp.sales.str.lower()
    emp = emp.join(pd.get_dummies(emp["sales"], prefix="dept"))
    emp = emp.join(pd.get_dummies(emp["salary"], prefix="salary"))
    emp = emp.drop(["empID", "salary_high", "dept_accounting", "sales", "salary"], axis = 1)
    return (emp, y)

def fit_model_pickle(data):
    """
    Takes a tuple with X matrix and Y vector as input. Fits a logistic regression on them.
    Then pickles the model for future use.

    :type data: tuple
    :param data: tuple with X matrix and Y vector for model fitting.
    """
    X = data[0]
    y = data[1]
    logreg = LogisticRegression()
    logreg.fit(X, y)
    #pickle the model
    pkl_filename = '../models/logistic.pkl'
    model_pkl = open(pkl_filename, 'wb')
    pickle.dump(logreg, model_pkl)
    model_pkl.close()

if __name__ == "__main__":
    fit_model_pickle(read_data())
