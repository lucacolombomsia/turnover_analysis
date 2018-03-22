import pandas as pd
import yaml
from sqlalchemy import create_engine
from time import localtime, strftime
import pickle
import numpy as np
import os
import sys
sys.path.insert(0, os.path.abspath('.'))
sys.path.append('develop/')
sys.path.append('develop/src')
from src import read_data, preprocess_for_sklearn
import src.dbconfig


def import_model():
    """Unpickle the model that was previously fit on the training data.

    Returns:
        The trained sklearn Logistic Regression model.
    """
    # read in the yaml file
    with open('params.yaml', 'r') as f:
        model_meta = yaml.load(f)

    # unpickle the model
    model_pkl = open(model_meta['directories']['pkl'], 'rb')
    model = pickle.load(model_pkl)
    model_pkl.close()
    return model


def read_prediction_form_data(form):
    """Read data inputted by the user in the Single Employee Evaluation form.

    Args:
        form: The form where the user can input the data.

    Returns:
        list: A list with the data read from the form.
    """
    #read the data
    entry1 = form.satisfaction.data
    entry2 = form.evaluation.data
    entry3 = form.projects.data
    entry4 = form.hours.data
    entry5 = form.tenure.data
    entry6 = form.accident.data
    entry7 = form.promotion.data
    entry8 = form.department.data
    entry9 = form.salary.data
    #store the data in a list
    data = [entry1, entry2, entry3, entry4, entry5,
            int(entry6), int(entry7), entry8, entry9]
    return data


def preprocess_prediction_form_data(form_data):
    """Preprocess data inputted by the user in the Single Employee
    Evaluation form.

    The data that has been read from the form must be preprocessed
    before being used for prediction.
    The model was fit using scikit learn, so categorical variables need to
    be transformed into dummies for the user input to be used for prediction.
    The output of this function is ready to be fed to the trained
    model and used for prediction.

    Args:
        form_data (list): A list with the data read from the form.

    Returns:
        A 2D numpy array with the processed data.
    """
    # will create a list with all the processed data
    # start with the first 7 elements (5 numerical variables and
    # 2 binary variables)
    mylist = form_data[0:7]
    # there are 10 categories (9 dummies) for the "department" variable
    # there are 3 possibile categories (2 dummies) for the "salary" variable
    # in total, 11 dummies ==> add 11 zeros
    mylist += [0]*11
    # notice that the form was setup in a way that form.department.data
    # and form.salary.data
    # are equal to the position of the list that needs to be set equal
    # to 1 based on the value chosen by the user in the form
    # can use values in entry8 and entry 9 to change the relevant dummy to 1!
    # Accounting is the reference category, so no dummy for it ==> the form
    # returns "drop" when user chooses accounting
    if (str(form_data[7]) != "drop"):
        mylist[int(form_data[7])] = 1
    # High is the reference category, so no dummy for it ==> the form
    # returns "drop" when user chooses high
    if (str(form_data[8]) != "drop"):
        mylist[int(form_data[8])] = 1
    # convert the list into a 2D np.array
    # this is required for the sklearn logistic regression to use the
    # data for prediction
    return np.array([mylist])


def write_prediction_form_data(form_data, prediction):
    """Write data inputted by the user to a database.

    Args:
        form_data (list): A list with the data read from the form.
        prediction (float): The predicted probability of quitting.
    """
    # will need the following dictionaries to convert output of form
    # into human readable data
    dept_dict = {"drop": "Accounting",
                 '7': "HR",
                 '8': "IT",
                 '9': "Management",
                 '10': "Marketing",
                 '11': "Product management",
                 '12': "R&D",
                 '13': "Sales",
                 '14': "Support",
                 '15': "Technical"}
    salary_dict = {"drop": "High",
                   '16': "Low",
                   '17': "Medium"}

    # first columns are easy, they are numerical/logical, nothing to modify
    names = ['satisfaction_level', 'last_eval', 'num_projects',
             'monthly_hours', 'tenure',
             'work_accident', 'promotion_last_5years']
    data = pd.DataFrame(data=[form_data[0:7]], columns=names)
    # make department and salary information readable using
    # dictionaries define above
    data["dept"] = dept_dict[form_data[7]]
    data["salary"] = salary_dict[form_data[8]]
    # add predicted probability to the dataframe
    data["predicted_proba"] = prediction
    # add timestamp to the dataframe
    data["timestamp"] = strftime("%Y-%m-%d %H:%M:%S", localtime())
    # write dataframe to database
    engine = create_engine(src.dbconfig.database_config)
    data.to_sql(name='user_input', con=engine,
                if_exists='append', index=False)


def give_promotion(data):
    """Modify data to study effect of promotion on probability of quitting.

    This is a support function for the give_recommendation function.
    It takes the output of preprocess_prediction_form_data as input.
    It modifies the preprocessed data to "give a promotion" to our
    employee of interest.
    Example: if salary was low, it raises it to medium by changing
    the appropriate categorical variable and setting the dummy for
    "received a promotion in last 5 years" to 1.
    The output of this function will be used to predict the effect of giving
    a promotion on the probability of quitting of our employee of interest.

    Args:
        data: Form data after preprocessing.

    Returns:
        Data in the same format as the input, but with different values.
    """
    # set dummy on promotion equal to 1
    data[0][6] = 1
    # if salary is low, make it medium
    if list(data[0][16:18]) == [1, 0]:
        data[0][16:18] = [0, 1]
    # if salary is medium, make it high
    elif list(data[0][16:18]) == [0, 1]:
        data[0][16:18] = [0, 0]
    return data

def increase_satisfaction(data):
    """Modify data to study effect of increase in satisfaction on
    probability of quitting.

    This is a support function for the give_recommendation function.
    It takes the output of preprocess_prediction_form_data as input.
    It modifies the preprocessed data by increasing the satisfaction
    of our employee of interest by 1/10 of a point.

    Args:
        data: Form data after preprocessing.

    Returns:
        Data in the same format as the input, but with different values.
    """
    data[0][0] = min(1, data[0][0] + 0.1)
    return data

def reduce_workload(data):
    """Modify data to study effect of reducing the workload on
    probability of quitting.

    This is a support function for the give_recommendation function.
    It takes the output of preprocess_prediction_form_data as input.
    It modifies the preprocessed data by reducing by 10% the number of 
    hours worked per month by our employee of interest.

    Args:
        data: Form data after preprocessing.

    Returns:
        Data in the same format as the input, but with different values.
    """
    data[0][3] = int(data[0][0]*0.9)
    return data


def give_recommendation(proba, model, data):
    """Give recommendation on action to take on evaluated user.

    Based on the predicted probability of quitting of the employee, suggest
    what actions should be taken (if any) to mitigate the risk of him/her
    quitting and how effective these actions are expected to be.

    Args:
        proba (float): predicted probability of quitting.
        model: model to be used for prediction.
        data: Form data after preprocessing.

    Returns:
        list: A list of strings with the recommended actions to be
        displayed in the results page.
    """
    if proba >= 50:
        text = ["""Historical data suggests that actions should be taken
                to reduce the risk that this employee will quit."""]
        text += ['Possible actions include:']
        # make prediction on the "new data", as modified by the
        # give_promotion function
        y_hat_promotion = model.predict_proba(give_promotion(data))[0][1]
        y_hat_promotion = round(y_hat_promotion*100, 2)
        # make prediction on the "new data", as modified by the
        # increase_satisfaction function
        y_hat_satisf = model.predict_proba(increase_satisfaction(data))[0][1]
        y_hat_satisf = round(y_hat_satisf*100, 2)
        # make prediction on the "new data", as modified by the
        # reduce_workload function
        y_hat_work = model.predict_proba(reduce_workload(data))[0][1]
        y_hat_work = round(y_hat_work*100, 2)

        # only report a suggestion if it actually decreases the probability
        # of quitting!!
        # to allow us to format the output in the html nicely, we need a
        # dictionary that stores text and predicted probability separately
        if proba > y_hat_promotion:
            y_hat_promotion = str(y_hat_promotion) + '%'
            text += [{'words': '''Offering a promotion; this would lower
            the probability of quitting to ''', 'num': y_hat_promotion}]

        if proba > y_hat_satisf:
            y_hat_satisf = str(y_hat_satisf) + '%'
            text += [{'words':'''Increasing the satisfaction level by one
            tenth of a point; this would lower the probability of
            quitting to ''', 'num': y_hat_satisf}]

        if proba > y_hat_work:
            y_hat_work = str(y_hat_work) + '%'
            text += [{'words': '''Reducing the workload by 10 percent;
            this would lower the probability of quitting to ''', 
            'num': y_hat_work}]

    # if the model classifies as non-quitter
    else:
        text = ["""It is unlikely that this employee will quit. No action
                needs to be taken."""]
    return text


def make_predictions(dbtable, model, n):
    """Predict probability of quitting of all employees in evaluation.

    Bulk load the data from a table in the database and predict for
    each employee the probability he/she will quit.
    The prediction is performed on the test data that was heldout from the
    original data.
    This is meant to simulate in-production data that comes from the annual
    or biannual company-wide employee evaluation.
    The function then returns a table with the n employees who are most
    likely to quit.

    Args:
        dbtable (str): name of the table to be queried for the bulk load.
        model: model to be used for prediction.
        n (int): number of results to be shown.

    Returns:
        pd.dataframe: The n employees who are most likely to quit.
    """
    # read the data
    data = read_data(dbtable)
    # preprocess it
    X_matrix = preprocess_for_sklearn(data)
    # make predictions and add predicted probability as a new column
    # to the original data after formatting
    predictions = list(model.predict_proba(X_matrix)[:, 1])
    y_pred = [round(x*100, 2) for x in predictions]
    data['phat'] = y_pred
    # sort by the predicted probability
    data = data.sort_values(by='phat', ascending=False)
    # return the n employees who are most likely to quit
    return data.head(n)


def format_predictions(table):
    """Format the table with the n most likely to quit employees.

    Take the output of make_predictions (a table with the n employees
    who are most likely to quit) and format it before it is shown to the
    user of the app.

    Args:
        table (pd.dataframe): Table with most likely to quit employees.

    Returns:
        pd.dataframe: The formatted dataframe.
    """
    # make promotion column yes/no instead of 0/1
    table['promotion'] = 'No'
    table.loc[table.promotion_last_5years == 1, 'promotion'] = 'Yes'
    # drop non-interesting columns
    table = table.drop(['number_project', 'phat',
                        'work_accident', 'promotion_last_5years'], axis=1)
    # change order of the columns
    order = ['emp_id', 'name', 'satisfaction_level', 'last_evaluation',
             'promotion', 'salary', 'average_montly_hours',
             'sales', 'time_spend_company']
    table = table[order]
    # make sure capitalization of words is nicely taken care of
    table.sales = table.sales.str.capitalize()
    table.loc[table.sales == 'Hr', 'sales'] = 'HR'
    table.loc[table.sales == 'Randd', 'sales'] = 'R&D'
    table.loc[table.sales == 'It', 'sales'] = 'IT'
    table.salary = table.salary.str.capitalize()
    # rename columns
    names = ['Employee ID', 'Name', 'Satisfaction Level', 'Last Evaluation',
             'Promotion in last 5 years', 'Salary category',
             'Monthly hours', 'Deparment',
             'Tenure in years']
    table.columns = names

    return table
