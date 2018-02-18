from flask import render_template, flash, redirect, url_for
from app import app
from app.forms import LoginForm
from app.functions import preprocess_form_data, import_model, make_predictions
from sklearn.linear_model import LogisticRegression

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        data = preprocess_form_data(form.satisfaction.data,
                                    form.evaluation.data,
                                    form.projects.data,
                                    form.hours.data,
                                    form.tenure.data,
                                    form.accident.data,
                                    form.promotion.data,
                                    form.department.data,
                                    form.salary.data)
        model = import_model()
        y_pred = round(model.predict_proba(data)[0][1]*100, 2)
        return render_template('thanks.html', perc=y_pred)
    return render_template('login.html', form=form)

@app.route('/table')
def table():
    model = import_model()
    pred_data = make_predictions('employees_eval_jan18', model, 10)
    return render_template('table.html',
      tables=[pred_data.to_html()], n = 10)