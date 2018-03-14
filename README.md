# Turnover Analysis

## Project Charter
A high turnover rate can seriously impact a company’s ability to be successful, as it causes high monetary costs and losses of human capital. The model developed in this project will predict the likelihood that current employees will leave the company and will therefore help understand what are the most relevant reasons behind an employee’s decision to voluntary terminate his employment – for example: low satisfaction, excessive workload, lack of career progression.   
The final goal of this project is to enable HR professionals and team managers to work conjunctly to retain the best talent.

**Vision**: increase employee retention and reduce the turnover rate, with a particular focus on reducing the number of high-performers that voluntarily leave.    

**Mission**: develop a model that evaluates the probability that each employee will quit and that helps inform the decision on whether or not to take action –and which action to take– to mitigate employee flight risk.    

**Success criteria**: the model can accurately predict the probability that an employee will quit, as measured by AUC, Recall and the Correct Classification Rate. 


## Package requirements
* [Flask](http://flask.pocoo.org/docs/0.12/). Flask is a microframework for web development in Python.
* [Jinja](http://jinja.pocoo.org/docs/2.10/templates/) for creating HTML templates with Python.
* [WTForms](https://wtforms.readthedocs.io/en/stable/). WTForms is a flexible forms validation and rendering library for Python.
* [SQLAlchemy](http://www.sqlalchemy.org/). SQLAlchemy is an Object Relational Mapper (ORM), which means it allows interaction with relational data models using object oriented approaches, like those typically used in Python. 
* [Psycopg](http://initd.org/psycopg/) for connecting to a Postgres database.
* [pandas](https://pandas.pydata.org/). pandas is an open source library that provides easy-to-use data structures and data analysis tools for Python.
* [scikit-learn](http://scikit-learn.org/stable/). scikit-learn provides simple and efficient tools for machine learning and data analysis in Python.

 
## Suggested steps to deploy app

1. Clone repository.

2. Create virtual environment and activate it:

    ```
    virtualenv -p python3 turnover
    source turnover/bin/activate
    ```
    

3. Install required packages:

    ```
    pip install -r requirements.txt
    ```

4. Set up turnover.env file with the following structure:

    ```
    export DATABASE=XXX
    export USERNAME=XXX
    export PORT=XXX
    export PASSWORD=XXX
    export HOST=XXX
    ```

5. Set environment variables from file:

    ```
    source turnover.env
    ```

6. Download the original data into the develop/data folder. The data was originally available on Kaggle, but it has since been removed; it can be downloaded from my Dropbox:

    ```
    wget -O develop/data/turnover.csv https://www.dropbox.com/s/qnu09f9xo30njvc/turnover.csv?dl=1
    ```

7. OPTIONAL STEP. If you want to run unit tests before running the code, you can do so by following the following instructions.

    ```
    cd develop/tests
    pytest
    cd ../..
    ```

8. Run the Makefile:

    ```
    make all
    ```

9. Launch the app:

    ```
    python webapp/turnover.py
    ```

You can then go to the IP address where the app is running and use the app.

## Pivotal tracker
The pivotal tracker page for this project can be reached by clicking on [this link](https://www.pivotaltracker.com/n/projects/2142055)