import pandas as pd
from sqlalchemy import create_engine
import config
from sklearn.model_selection import train_test_split

def make_employees_table() :
    """
    Reads the training data from csv and writes it to employees table in database
    """
    employees = pd.read_csv('../data/turnover.csv')
    employees.insert(0, 'emp_ID', range(1, len(employees)+1))
    train, test = train_test_split(employees, test_size=1000, random_state = 12345)
    test = test.reset_index(drop=True)
    test = test.join(pd.read_csv("../data/random-names.csv"))
    engine = create_engine(config.database_config)
    train.to_sql(name = 'employees_hist_data', con = engine, if_exists='replace', index=False)
    test.to_sql(name = 'employees_new_data', con = engine, if_exists='replace', index=False)

if __name__ == "__main__":
    make_employees_table()
