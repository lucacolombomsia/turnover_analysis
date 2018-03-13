import dbconfig
from sqlalchemy import create_engine
import pandas as pd


def read_data(table_name):
    """Read the data from a specified table in the database.

    This function can be used to query both the train set (used to fit model)
    and the "in-production" data (used to make bulk predictions).
    This function will always return a dataframe with all columns stored
    in the table that it is asked to query.

    Args:
        table_name (str): Name of table to be queried

    Returns:
        pandas.DataFrame: A dataframe with the data read from database.
    """
    engine = create_engine(dbconfig.database_config)
    sql = "select * from " + table_name
    data = pd.read_sql_query(sql, con=engine)
    return data


def preprocess_for_sklearn(data):
    """Preprocess the data into a format compatible with sklearn.

    Sklearn requires all categorical variables to be converted
    into dummies.
    The input is a dataframe of predictors, either from the train
    or the in-production data.

    Args:
        data (pd.dataframe): The dataframe with the data to be preprocessed.

    Returns:
        pd.dataframe: A dataframe with the processed data.
    """
    data.columns = map(str.lower, data.columns)
    data.sales = data.sales.str.lower()
    # create dummies for categorical variables
    data = data.join(pd.get_dummies(data["sales"], prefix="dept"))
    data = data.join(pd.get_dummies(data["salary"], prefix="salary"))
    # drop variables that should not be in the X matrix
    # these include: employer ID, categorical variables that have
    # been converted into dummies and one dummy per each
    # categorical variable (to avoid perfect multicollinearity)
    data = data.drop(["emp_id", "salary_high", "dept_accounting",
                      "sales", "salary"], axis=1)
    # the test data has an extra column compared to the train data
    # it's the name of the employee and it has to be dropped
    try:
        data = data.drop(["name"], axis=1)
    except ValueError:
        pass
    return data
