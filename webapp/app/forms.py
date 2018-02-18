from flask_wtf import FlaskForm
from wtforms import FloatField, IntegerField, BooleanField, SelectField, SubmitField, DateField
from wtforms.validators import DataRequired, NumberRange, StopValidation
from datetime import datetime as dt

class LoginForm(FlaskForm):
    satisfaction = FloatField('Satisfaction Level',
        validators=[DataRequired(), NumberRange(min=0, max=1)])
    evaluation = FloatField('Last Evaluation', 
        validators=[DataRequired(), NumberRange(min=0, max=1)])
    projects = IntegerField('Number of projects',
        validators=[NumberRange(min=1, message="An integer larger than 0")])
    hours = IntegerField('Average monthly hours',
        validators=[NumberRange(min=1, message="An integer larger than 0")])
    tenure = IntegerField('Tenure',
        validators=[NumberRange(min=1, message="An integer larger than 0")])
    accident = BooleanField('Work Accident')
    promotion = BooleanField('Promotion in last 5 years')
    department = SelectField('Department', 
        choices=[('drop', "Accounting"),
                 ('7', "HR"),
                 ('8', "IT"),
                 ('9', "Management"),
                 ('10', "Marketing"),
                 ('11', "Product Management"),
                 ('12', "R&D"),
                 ('13', "Sales"),
                 ('14', "Support"),
                 ('15', "Technical")],
        validators=[DataRequired()])
    salary = SelectField('Salary', 
        choices=[('16', "Low"),
                 ('17', "Medium"),
                 ('drop', "High")],
        validators=[DataRequired()])
    submit = SubmitField('Submit')

def validate_dates(form, field):
        if (field.data != dt.strptime('2018-01', '%Y-%m').date() and 
           field.data != dt.strptime('2017-07', '%Y-%m').date()):
            raise StopValidation('No employee evaluation on this date')

class DatabaseForm(FlaskForm):
    date = DateField('Month and year of last Employee Evaluation',
        format='%Y-%m', validators=[validate_dates])
    number = IntegerField('Number of results to display',
        validators=[NumberRange(min=1, message="An integer larger than 0")])
    submit = SubmitField('Submit')