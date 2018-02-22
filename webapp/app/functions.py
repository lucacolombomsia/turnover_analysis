import pickle
import numpy as np
import os, sys
sys.path.insert(0, os.path.abspath('.'))
sys.path.append('../develop/')
sys.path.append('../develop/src')
from src import read_data, preprocess_for_sklearn
from sklearn.linear_model import LogisticRegression
import pandas as pd

def import_model():
    """
    Unpickles the model that was previously fit on the training data.

    Returns:
        The trained sklearn Logistic Regression model.
    """
    pkl_filename = '../develop/models/logistic.pkl'
    model_pkl = open(pkl_filename, 'rb')
    model = pickle.load(model_pkl)
    model_pkl.close()
    return model

def preprocess_prediction_form_data(form):
    """ Reads and preprocesses data inputted by the user in the form .   
    
    The user inputs data in the form on the app.
    The data is then read and must be preprocessed before being used for prediction.
    The model was fit using scikit learn, so categorical variables need to be transformed into dummies
    for the user input to be used for prediction.
    The output of this is ready to be fed into the model and used for prediction.

    Args:
        form: The form where the user can input the data.

    Returns:
        A 2D numpy array with the processed data, that can be fed into the sklearn model.
    """

    #"form" is an instance of a class that inherits from a FlaskForm
    #can easily read data by simply accessing the right methods
    entry1 = form.satisfaction.data
    entry2 = form.evaluation.data
    entry3 = form.projects.data
    entry4 = form.hours.data
    entry5 = form.tenure.data
    entry6 = form.accident.data
    entry7 = form.promotion.data
    entry8 = form.department.data
    entry9 = form.salary.data

    #will create a list with all the processed data
    #start by adding the first 7 elements (5 numerical variables + 2 binary variables)
    mylist = [entry1, entry2, entry3, entry4, entry5, int(entry6), int(entry7)]
    #there are 10 possible categories (9 dummies) for the "department" variable
    #there are 3 possibile categories (2 dummies) for the "salary" variable
    #in total, 11 dummies ==> add 11 zeros
    mylist += [0]*11
    #notice that the form was setup in a way that form.department.data and form.salary.data
    #are equal to the position of the list that needs to be set equal to 1 based on the value chosen
    #by the user in the form
    #can use values in entry8 and entry 9 to change the relevant dummy to 1!
    #Accounting is the reference category, so no dummy for it ==> form returns "drop" when
    #user chooses accounting
    if (str(entry8)!="drop"):
        mylist[int(entry8)] = 1
    #High is the reference category, so no dummy for it ==> form returns "drop" when
    #user chooses high
    if (str(entry9)!="drop"):
        mylist[int(entry9)] = 1
    #convert the list into a 2D np.array
    #this is required for the sklearn logistic regression to use the data for prediction
    return np.array([mylist])

def give_promotion(data):
    """
    Support function for the give_recommendation function.
    It takes the output of preprocess_prediction_form_data as input.
    It modifies the processed data to "give a promotion" to our employee of interest.
    Example: if salary was low, it raises it to medium by changing the appropriate dummy and setting the
    dummy for "received a promotion in last 5 years" to 1.
    The output of this function will be used to predict the effect of giving a promotion on the
    probability of quitting of our employee of interest.

    Args:
        data: Form data preprocessed by the preprocess_prediction_form_data function.

    Returns:
        Form data in the same format as the input, but with different values.
    """
    #set dummy on promotion equal to 1
    data[0][6] = 1
    #if salary is low, make it medium
    if list(data[0][16:18]) == [1,0]:
        data[0][16:18] = [0,1]
    #if salary is medium, make it high
    elif list(data[0][16:18]) == [0,1]:
        data[0][16:18] = [0,0]
    return data

def give_recommendation(proba, model, data):
    """
    Based on the predicted probability of quitting of the employee, suggest what actions should be taken
    (if any) to mitigate the risk of him/her quitting and how effective these actions are expected to be.
    
    Args:
        proba (float): predicted probability of quitting.
        model: model to be used for prediction.
        data: Form data preprocessed by the preprocess_prediction_form_data function.

    Returns:
        list: A list of strings with the recommended actions to be displayed in the results page.
    """
    #historical data suggests that the company should act whenever the predicted probability of
    #quitting is above 25%
    if proba > 25:
        text = ["""Historical data suggests that actions should be taken to reduce the risk
        of an employee quitting whenever his or her predicted probability of quitting is
        above 25%."""]
        #make prediction on the "new data", as modified by the give_promotion function
        y_hat_prime = round(model.predict_proba(give_promotion(data))[0][1]*100, 2)
        if proba != y_hat_prime:
            text += ['''Offering a promotion to this employee would lower
            the probability with which he or she will quit to {}%'''.format(y_hat_prime)]
    else:
        text = ["It is unlikely that this employee will quit. No action needs to be taken."]
    return text

def make_predictions(dbtable, model, n):
    """
    Bulk loads the data from a table in the AWS database and predicts for each employee
    the probability he/she will quit.
    The prediction is performed on the test data that we heldout from the original data.
    This is meant to simulate in-production data that comes from the annual or biannual 
    company-wide employee evaluation.
    The function then returns a table with the n employees who are most likely to quit.

    Args:
        dbtable (str): name of the table to be queried for the bulk load.
        model: model to be used for prediction.
        n (int): number of results to be shown.

    Returns:
        dataframe: A dataframe with the n employees who are most likely to quit.
    """
    #read the data
    data = read_data(dbtable)
    #preprocess it
    X_matrix = preprocess_for_sklearn(data)
    #make predictions and add predicted probability as a new column to the original data
    y_pred = pd.DataFrame({"phat" : model.predict_proba(X_matrix)[:,1]})
    data = data.join(y_pred)
    #sort by the predicted probability
    data = data.sort_values(by='phat', ascending = False)
    #return the n employees who are most likely to quit
    return data.head(n)

