import dbconfig
from sqlalchemy import create_engine
import pandas as pd


def read_data(table_name):
    """
    Reads the data from a specified table in the database.
    It can be used to query both the train and the test set.
    When asked to read the table that contains the training data, it will
    return a tuple with the data from all the predictors (the X matrix) and
    the data for the response (the Y vector).
    When asked to read a table that contains the test data, it will return a
    pandas dataframe with the data from all the predictors (the X matrix).

    Args:
        table_name (str): Name of table to be queried
    """
    engine = create_engine(dbconfig.database_config)
    sql = "select * from " + table_name
    data = pd.read_sql_query(sql, con=engine)
    # if the data contains the column "left" (the response), we have queried
    # the training set; if the data doesn't contain
    # the column "left", we have queried one of the test sets
    try:
        y = data.left
        data = data.drop(["left"], axis=1)
        return (data, y)
    except AttributeError:
        return data


def preprocess_for_sklearn(data):
    """
    Preprocesses the data for all the predictors into a format that is
    compatible with sklearn, by converting all categorical variables
    into dummies.
    The preprocessed data can be used both to train the model and to
    make predictions on the test set.

    Args:
        data (dataframe): The dataframe with the data to be preprocessed.

    Returns:
        dataframe: A dataframe with the processed data.
    """
    data.columns = map(str.lower, data.columns)
    data.sales = data.sales.str.lower()
    # create dummies for categorical variables
    data = data.join(pd.get_dummies(data["sales"], prefix="dept"))
    data = data.join(pd.get_dummies(data["salary"], prefix="salary"))
    # drop variables that should not be in the X matrix
    # these include: employer ID, categorical vars and one dummy
    # per category (to avoid perfect multicollinearity)
    data = data.drop(["emp_id", "salary_high", "dept_accounting",
                      "sales", "salary"], axis=1)
    # the test data has an extra column compared to the train data
    # it's the name of the employee and it has to be dropped
    try:
        data = data.drop(["name"], axis=1)
    except ValueError:
        pass
    return data
