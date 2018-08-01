import os

dbname = os.environ.get('DATABASE')
user = os.environ.get('USERNAME')
host = os.environ.get('HOST')
port = os.environ.get('PORT')
pw = os.environ.get('PASSWORD')

database_config = ("postgresql://" + user + ":" + pw +
                   "@" + host + ":" + port + "/" + dbname)
