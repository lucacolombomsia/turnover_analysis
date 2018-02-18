from flask import render_template, flash, redirect, url_for
from app import app
from app.forms import LoginForm, DatabaseForm
from app.functions import preprocess_form_data, import_model, make_predictions
from sklearn.linear_model import LogisticRegression
from datetime import datetime as dt

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        data = preprocess_form_data(form)
        model = import_model()
        y_pred = round(model.predict_proba(data)[0][1]*100, 2)
        return render_template('thanks.html', perc=y_pred)
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
      pred_data = make_predictions(table = data, model = model, n = num)
      return render_template('table.html', tables=[pred_data.to_html()],
                              date = date_str, n = num)
    return render_template('database_form.html', form = form)