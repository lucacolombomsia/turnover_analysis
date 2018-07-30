import os

dbname = os.environ.get('DATABASE')
user = os.environ.get('USERNAME')
host = os.environ.get('HOST')

database_config = ("postgresql://" + user + "@" + host + "/" + dbname)

'''database_config = ("postgresql://" + user + ":" + pw +
                   "@" + host + ":" + port + "/" + dbname)'''
