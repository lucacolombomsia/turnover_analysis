import pickle
import numpy as np
import os, sys
sys.path.insert(0, os.path.abspath('.'))
sys.path.append('../develop/')
sys.path.append('../develop/src')
from src import read_data, preprocess_for_sklearn
from sklearn.linear_model import LogisticRegression
import pandas as pd

def preprocess_form_data(form):

    """ Preprocesses data inputted by the user in the flask app.   
    
    The user inputs data in the form on the flask app. The data is then read and must be preprocessed before
    being used for prediction.
    The model was fit using scikit learn, so categorical variables need to be transformed into dummies
    for the user input to be used for prediction.
    The output of this function contains all necessary dummies and is ready to be fed into the model.

    Args:
        a_orig (list): A list with the user input read from the form.

    Returns:
        list: A list with the processed data.
    """

    entry1 = form.satisfaction.data
    entry2 = form.evaluation.data
    entry3 = form.projects.data
    entry4 = form.hours.data
    entry5 = form.tenure.data
    entry6 = form.accident.data
    entry7 = form.promotion.data
    entry8 = form.department.data
    entry9 = form.salary.data

    #keep only the first 7 elements (5 numerical variables + 2 binary variables)
    mylist = [entry1, entry2, entry3, entry4, entry5, int(entry6), int(entry7)]
    #there are 10 possible categories (9 dummies) for the "department" variable
    #there are 3 possibile categories (2 dummies) for the "salary" variable
    #in total, 11 dummies ==> add 11 zeros, then will use dictionary to change the relevant dummy to 1
    mylist += [0]*11
    #Accounting is the reference category, so no dummy for it (to avoid perfect multicollinearity)
    if (str(entry8)!="drop"):
        mylist[int(entry8)] = 1
    #High is the reference category, so no dummy for it (to avoid perfect multicollinearity)
    if (str(entry9)!="drop"):
        mylist[int(entry9)] = 1
    mylist += [mylist[6]*mylist[3]]
    mylist += [mylist[6]*mylist[4]]
    return np.array([mylist])

def import_model():
    pkl_filename = '../develop/models/logistic.pkl'
    model_pkl = open(pkl_filename, 'rb')
    model = pickle.load(model_pkl)
    model_pkl.close()
    return model

def make_predictions(table, model, n = 5):
    data = read_data(table)
    X_matrix = preprocess_for_sklearn(data)[0]
    y_pred = pd.DataFrame({"phat" : model.predict_proba(X_matrix)[:,1]})
    data = data.join(y_pred)
    data = data.sort_values(by='phat', ascending = False)
    return data.head(n)



