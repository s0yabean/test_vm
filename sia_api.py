import pandas as pd
from flask import Flask, request
from flask_restful import Resource, Api
from sqlalchemy import create_engine
from json import dumps

#Create a engine for connecting to SQLite3.
#Assuming salaries.db is in your app root folder

connection_strings = {
    "sia_app" : "postgres://oehrcduj:1bZl-rS-k6mVxgRSKzE1cFZa1KXTb8bR@elmer.db.elephantsql.com:5432/oehrcduj"
}

def get_engine(db='sia_app'):
    return create_engine(connection_strings[db], connect_args={"application_name": "sia_app"})

def get_connection(db='sia_app'):
    attempts = 0
    while attempts < 3:
        try:
            engine = get_engine(db)
            return engine.raw_connection()
        except Exception as e:
            attempts += 1
            time.sleep(20)

e = get_engine()

app = Flask(__name__)
api = Api(app)

class get_data(Resource):
    def get(self):
        #Connect to databse
        conn = e.connect()
        #Perform query and return JSON data
        query = "select * from public.sia_app_db"
        df = pd.read_sql(query, conn)
        json = df.to_json()
        return json

class post_data(Resource):
    def post(self):
        conn = e.connect()
        query = "select * from public.sia_app_db"
        #Query the result and get cursor.Dumping that data to a JSON is looked by extension
        df = pd.read_sql(query, conn)
        json = df.to_json()
        return json
        #We can have PUT,DELETE,POST here. But in our API GET implementation is sufficient
 
api.add_resource(get_data, '/get_data')
api.add_resource(post_data, '/post_data')

if __name__ == '__main__':
     app.run()