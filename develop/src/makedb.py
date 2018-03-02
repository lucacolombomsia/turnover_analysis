import pandas as pd
from sqlalchemy import create_engine
import dbconfig
from sklearn.model_selection import train_test_split
import logging

def make_tables() :
    """
    Reads the training data from csv.
    Randomly splits the data in one training set and two test sets.
    Writes each dataset to a different table in the database.
    """
    #setup log file
    log_fmt = '%(asctime)s - %(levelname)s - %(message)s'
    logging.basicConfig(filename='develop/logs/makedb.log', level=logging.INFO, format=log_fmt)
    logger = logging.getLogger(__name__)

    employees = pd.read_csv('develop/data/turnover.csv')
    employees.insert(0, 'emp_ID', range(1, len(employees)+1))
    #holdout 1000 observation for bulk-loading and making prediction
    #this heldout data will simulate in-production data
    train, test = train_test_split(employees, test_size=1000, random_state = 12345)
    test = test.reset_index(drop=True)
    #for test data, we add a name to each employee
    test = test.join(pd.read_csv("develop/data/random-names.csv"))
    #drop the Y variable for the test data, so that it can play the role of in-production data
    #this data will be used for bulk-load predictions
    test = test.drop(["left"], axis = 1)
    jul17, jan18 = train_test_split(test, test_size=500, random_state = 12345)
    engine = create_engine(dbconfig.database_config)
    logger.info('Created engine')
    jul17.to_sql(name = 'employees_eval_jul17', con = engine, if_exists='replace', index=False)
    logger.info('Wrote test set July 2017')
    jan18.to_sql(name = 'employees_eval_jan18', con = engine, if_exists='replace', index=False)
    logger.info('Wrote test set January 2018')
    train.to_sql(name = 'employees_hist_data', con = engine, if_exists='replace', index=False)
    logger.info('Wrote train set')

if __name__ == "__main__":
    make_tables()
