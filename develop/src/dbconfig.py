import os

dbname = os.environ.get('DATABASE')
user = os.environ.get('USERNAME')
port = os.environ.get('PORT')
pw = os.environ.get('PASSWORD')
host = os.environ.get('HOST')

database_config = ("postgresql://" + user + ":" + pw +
                   "@" + host + ":" + port + "/" + dbname)
