from flask_wtf import FlaskForm
from wtforms import FloatField, IntegerField, BooleanField, SelectField, SubmitField, DateField
from wtforms.validators import DataRequired, NumberRange, StopValidation
from datetime import datetime as dt

class PredictionForm(FlaskForm):
    """
    The form that will be used to collect the user input to make predictions on a single employee.
    """
    satisfaction = FloatField('Satisfaction Level',
        validators=[DataRequired(), NumberRange(min=0, max=1)])
    evaluation = FloatField('Last Evaluation', 
        validators=[DataRequired(), NumberRange(min=0, max=1)])
    projects = IntegerField('Number of projects',
        validators=[NumberRange(min=1, message="Please input an integer larger than 0")])
    hours = IntegerField('Average monthly hours',
        validators=[NumberRange(min=1, message="Please input an integer larger than 0")])
    tenure = IntegerField('Tenure',
        validators=[NumberRange(min=1, message="Please input an integer larger than 0")])
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
    """
    A custom validator for the date field in the DatabaseForm.
    It makes sure that the user inputs a valid date, ie a date on which an employee evaluation
    was conducted by the company.
    """
    if (field.data != dt.strptime('2018-01', '%Y-%m').date() and 
       field.data != dt.strptime('2017-07', '%Y-%m').date()):
        raise StopValidation('No employee evaluation on this date')

class DatabaseForm(FlaskForm):
    """
    The form that will be used to collect the user input regarding the bulk load prediction.
    The user can choose the date of the employee evaluation of interest and the number of results to be displayed.
    """
    date = DateField('Month and year of Employee Evaluation of interest',
        format='%Y-%m', validators=[validate_dates])
    number = IntegerField('Number of results to display',
        validators=[NumberRange(min=1, message="An integer larger than 0")],
        default=10)
    submit = SubmitField('Submit')