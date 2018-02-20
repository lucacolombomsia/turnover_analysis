import pandas as pd
from sqlalchemy import create_engine
import secret_config
from sklearn.model_selection import train_test_split

def make_tables() :
    """
    Reads the training data from csv and writes it to employees table in database
    """
    employees = pd.read_csv('../data/turnover.csv')
    employees.insert(0, 'emp_ID', range(1, len(employees)+1))
    train, test = train_test_split(employees, test_size=1000, random_state = 12345)
    test = test.reset_index(drop=True)
    test = test.join(pd.read_csv("../data/random-names.csv"))
    test = test.drop(["left"], axis = 1)
    jul17, jan18 = train_test_split(test, test_size=500, random_state = 12345)
    engine = create_engine(secret_config.database_config)
    jul17.to_sql(name = 'employees_eval_jul17', con = engine, if_exists='replace', index=False)
    print("Done")
    jan18.to_sql(name = 'employees_eval_jan18', con = engine, if_exists='replace', index=False)
    print("Done")
    train.to_sql(name = 'employees_hist_data', con = engine, if_exists='replace', index=False)
    
if __name__ == "__main__":
    make_tables()
