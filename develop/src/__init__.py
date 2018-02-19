import secret_config
from sqlalchemy import create_engine
import pandas as pd

def read_data(table_name):
    """
    Reads the data from the employees table in the DB. Then preprocesses data for model fitting and 
    returns a tuple with the X matrix and Y vector (in that order).

    Returns:
        tuple: A tuple with the X matrix and the Y vector.
    """
    engine = create_engine(secret_config.database_config)
    sql = "select * from " + table_name
    data = pd.read_sql_query(sql, con = engine)
    print("Successfully read data")
    return data

def preprocess_for_sklearn(data):
    y = data['left']
    data.columns = map(str.lower, data.columns)
    data.sales = data.sales.str.lower()
    #create dummies for categorical variables
    data = data.join(pd.get_dummies(data["sales"], prefix="dept"))
    data = data.join(pd.get_dummies(data["salary"], prefix="salary"))
    #drop variables that should not be in the X matrix
    #these include: left (ie the target variable), employer ID, categorical vars and
    #one dummy per category (to avoid perfect multicollinearity)
    data = data.drop(["left", "emp_id", "salary_high", "dept_accounting", "sales", "salary"], axis = 1)
    try:
        data = data.drop(["name"], axis = 1)
    except:
        pass
    return (data, y)