import secret_config
from sqlalchemy import create_engine
import pandas as pd

def read_data(table_name):
    """
    Reads the data from a specified table in the database. 
    
    Args:
        table_name (str): Name of table to 

    Returns:
        dataframe: A pandas dataframe with the data.
    """
    engine = create_engine(secret_config.database_config)
    sql = "select * from " + table_name
    data = pd.read_sql_query(sql, con = engine)
    try:
        y = data.left
        data = data.drop(["left"], axis = 1)
        return (data, y)
    except:
        return data

def preprocess_for_sklearn(data):
    """
    Preprocesses data into a format that is compatible with sklearn.
    The preprocessed data can be used both to train the model and to make predictions on the test set.
    It returns a tuple with the X matrix and Y vector (in that order).

    Args:
        data (dataframe): The dataframe with the data to be preprocessed.

    Returns:
        tuple: A tuple with the X matrix and the Y vector.
    """
    data.columns = map(str.lower, data.columns)
    data.sales = data.sales.str.lower()
    #create dummies for categorical variables
    data = data.join(pd.get_dummies(data["sales"], prefix="dept"))
    data = data.join(pd.get_dummies(data["salary"], prefix="salary"))
    #drop variables that should not be in the X matrix
    #these include: left (ie the target variable), employer ID, categorical vars and
    #one dummy per category (to avoid perfect multicollinearity)
    data = data.drop(["emp_id", "salary_high", "dept_accounting", "sales", "salary"], axis = 1)
    try:
        data = data.drop(["name"], axis = 1)
    except:
        pass
    return data
