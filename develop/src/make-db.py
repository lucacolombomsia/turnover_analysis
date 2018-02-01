import pandas as pd
from sqlalchemy import create_engine
import config

def make_local_db() :
    employees = pd.read_csv('../data/turnover.csv')
    print(employees.shape)
    engine = create_engine(config.database_config)
    employees.to_sql(name = 'employees', con = engine, if_exists='replace')

if __name__ == "__main__":
    make_local_db()
