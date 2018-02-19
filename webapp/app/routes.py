from flask import render_template, flash, redirect, url_for
from app import app
from app.forms import PredictionForm, DatabaseForm
from app.functions import preprocess_prediction_form_data, import_model, make_predictions, give_promotion, give_recommendation
from sklearn.linear_model import LogisticRegression
from datetime import datetime as dt

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/single_emp', methods=['GET', 'POST'])
def single_emp():
    form = PredictionForm()
    if form.validate_on_submit():
        data = preprocess_prediction_form_data(form)
        model = import_model()
        y_pred = round(model.predict_proba(data)[0][1]*100, 2)
        text = give_recommendation(y_pred, model, data)
        return render_template('thanks.html', perc=y_pred, sentences = text)
    return render_template('login.html', form=form)

@app.route('/table', methods=['GET', 'POST'])
def table():
    form = DatabaseForm()
    if form.validate_on_submit():
        num = form.number.data
        date_str = form.date.data.strftime('%B %Y')
        if form.date.data == dt.strptime('2018-01', '%Y-%m').date():
            data = 'employees_eval_jan18'
        if form.date.data == dt.strptime('2017-07', '%Y-%m').date():
            data = 'employees_eval_jul17'
        model = import_model()
        pred_data = make_predictions(dbtable = data, model = model, n = num)
        return render_template('table.html', tables=[pred_data.to_html()],
                              date = date_str, n = num)
    return render_template('database_form.html', form = form)
