from pymongo import MongoClient
import configparser
import os

_config = configparser.ConfigParser()
_config.read(os.path.join(os.path.dirname(__file__), 'dbconfig.ini'))
_conn_str = "mongodb+srv://{user}:{password}@{host}/{db}?retryWrites=true&w=majority"
_conn = MongoClient(_conn_str.format(user=_config['mongoDB']['user'], password=_config['mongoDB']['pass'],
                                     host=_config['mongoDB']['host'], db=_config['mongoDB']['db']))

db = _conn.Probaz
items_collection= db.items
users_collection = db.users
