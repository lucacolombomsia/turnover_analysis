from flask import render_template, flash, redirect, url_for
from app import app
from app.forms import PredictionForm, DatabaseForm
from app.functions import preprocess_prediction_form_data, import_model, make_predictions, give_promotion, give_recommendation
from sklearn.linear_model import LogisticRegression
from datetime import datetime as dt

@app.route('/')
@app.route('/index')
def index():
    return render_template('homepage.html')

@app.route('/single_emp', methods=['GET', 'POST'])
def single_emp():
    #create instance of PredictionForm class
    form = PredictionForm()
    #if the WTForm validators validate:
    if form.validate_on_submit():
        #preprocess the form data
        data = preprocess_prediction_form_data(form)
        #unpickle the model
        model = import_model()
        #predict probability of quitting
        y_pred = round(model.predict_proba(data)[0][1]*100, 2)
        #given the predicted proba, what is the best course of action?
        #use the giverecommendation function to find out
        text = give_recommendation(y_pred, model, data)
        #show results
        return render_template('single_results.html', perc=y_pred, sentences = text)
    return render_template('single_form.html', form=form)

@app.route('/table', methods=['GET', 'POST'])
def table():
    #create instance of DatabaseForm class
    form = DatabaseForm()
    #if the WTForm validators validate:
    if form.validate_on_submit():
        #get the number of results the user wants to see
        num = form.number.data
        #based on the user input, choose the right table in the database to be queried
        date_str = form.date.data.strftime('%B %Y')
        if form.date.data == dt.strptime('2018-01', '%Y-%m').date():
            data = 'employees_eval_jan18'
        if form.date.data == dt.strptime('2017-07', '%Y-%m').date():
            data = 'employees_eval_jul17'
        #unpickle the model
        model = import_model()
        #make prediciton on bulk load of data from database
        pred_data = make_predictions(dbtable = data, model = model, n = num)
        #show results
        return render_template('bulk_results.html', tables=[pred_data.to_html(classes='tab', index = False)],
                              date = date_str, n = num)
    return render_template('bulk_form.html', form = form)
