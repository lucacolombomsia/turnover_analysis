from flask import Flask, render_template, request
import os, sys
sys.path.insert(0, os.path.abspath('.'))
sys.path.append('../develop')
from src import preprocess
import pickle
from sklearn.linear_model import LogisticRegression
import numpy as np

def read_data_in_form():
    x = [round(float(request.form['satisfaction']),2)]
    x += [round(float(request.form['evaluation']),2)]
    x += [round(float(request.form['projects']), 2)]
    x += [round(float(request.form['hours']), 2)]
    x += [round(float(request.form['tenure']), 2)]
    x += [request.form.get('accident')]
    x += [request.form.get('promotion')]
    x += [request.form.get('department')]
    x += [request.form.get('salary')]
    x = np.array([preprocess.preprocess(x)])
    return x

def import_model():
    pkl_filename = '../develop/models/logistic.pkl'
    model_pkl = open(pkl_filename, 'rb')
    model = pickle.load(model_pkl)
    model_pkl.close()
    return model

app = Flask(__name__)

@app.route('/')
def index():
    return 'This is the homepage'

@app.route("/inputs")
def my_form():
    return render_template('my-form.html')

@app.route('/inputs', methods=['POST'])
def my_form_post():
    x = read_data_in_form()
    model = import_model()
    #predict proba returns a list of list
    #I want the second element of the first list (ie the predicted probability of Y == 1)
    y_pred = round(model.predict_proba(x)[0][1]*100, 2)
    return "The employee will quit with a probability of {}%".format(str(y_pred))

if __name__ == "__main__":
    app.run(debug=True)
