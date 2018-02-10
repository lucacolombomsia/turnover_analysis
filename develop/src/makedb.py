import pandas as pd
from sqlalchemy import create_engine
import config

def make_employees_table() :
    """
    Reads the training data from csv and writes it to employees table in database
    """
    employees = pd.read_csv('../data/turnover.csv')
    employees.insert(0, 'empID', range(1, len(employees)+1))
    engine = create_engine(config.database_config)
    employees.to_sql(name = 'employees', con = engine, if_exists='replace', index=False)
    print("Created employees table")

if __name__ == "__main__":
    make_employees_table()
