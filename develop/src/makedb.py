import pandas as pd
from sqlalchemy import create_engine
import dbconfig
from sklearn.model_selection import train_test_split
import logging
import argparse
import yaml


def prep_tables():
    """
    Read the training data from csv.
    Randomly split the data in one training set and two test sets.
    The two test sets will simulate in-production data and will be
    queried by the web app.
    Since they will be used for prediction, drop response variable
    for all observations in the test sets.
    Also, add fake name to each employee in the test sets to better
    simulate in-production data.

    This is a support function for write_tables.
    It returns 3 dataframes that write_tables will write into a
    database.

    Returns:
        tuple: A tuple with the 3 dataframes.

    """
    # get logger
    logger = logging.getLogger(__name__)
    employees = pd.read_csv(model_meta['directories']['train_data'])
    logger.info('Read data from CSV')
    employees.insert(0, 'emp_ID', range(1, len(employees)+1))
    # holdout 1000 observation for bulk-loading and making prediction
    # this heldout data will simulate in-production data
    train, test = train_test_split(employees,
                                   test_size=int(model_meta['test_size']),
                                   random_state=model_meta['random'])
    logger.info('Split train and test')
    test = test.reset_index(drop=True)
    # for test data, we add a name to each employee
    test = test.join(pd.read_csv(model_meta['directories']['names']))
    # drop the Y variable for the test data, so that it can play
    # the role of in-production data
    # this data will be used for bulk-load predictions
    test = test.drop(["left"], axis=1)
    logger.info('Transformed test data into fake in-production data')
    jul17, jan18 = train_test_split(test,
                                    test_size=int(model_meta['test_size']/2),
                                    random_state=model_meta['random'])
    logger.info('Data ready to be written to db')
    return (train, jul17, jan18)


def write_tables():
    """
    Take the output of the function prep_tables (3 dataframes) and write each
    of them in a different table in the database.
    """
    # get logger
    logger = logging.getLogger(__name__)

    # prepare tables using helper function
    train, jul17, jan18 = prep_tables()
    
    engine = create_engine(dbconfig.database_config)
    logger.info('Created engine for writing')
    jul17.to_sql(name='employees_eval_jul17', con=engine,
                 if_exists='replace', index=False)
    logger.info('Wrote test set July 2017')
    jan18.to_sql(name='employees_eval_jan18', con=engine,
                 if_exists='replace', index=False)
    logger.info('Wrote test set January 2018')
    train.to_sql(name='employees_hist_data', con=engine,
                 if_exists='replace', index=False)
    logger.info('Wrote train set')


if __name__ == "__main__":
    # handle command line arguments (location of yaml file)
    parser = argparse.ArgumentParser()
    parser.add_argument('meta_path', help="path of the yaml file")
    args = parser.parse_args()
    #read in the yaml file
    with open(args.meta_path, 'r') as f:
        model_meta = yaml.load(f)

    # setup log file
    log_fmt = '%(asctime)s - %(levelname)s - %(message)s'
    logging.basicConfig(filename=model_meta['directories']['log'],
                        level=logging.INFO, format=log_fmt)
    logger = logging.getLogger(__name__)

    write_tables()
