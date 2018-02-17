import pickle
import numpy as np

def preprocess(entry1, entry2, entry3, entry4, entry5, entry6, entry7, entry8, entry9):
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

    #keep only the first 7 elements (5 numerical variables + 2 binary variables)
    mylist = [entry1, entry2, float(entry3), float(entry4),
                float(entry5), int(entry6), int(entry7)]
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