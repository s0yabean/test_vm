import pandas as pd
import csv
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy import create_engine
from sqlalchemy import text, Column, Float, Integer, String, DateTime, Numeric, Date, Boolean, JSON, Time
from time import sleep

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

Base = declarative_base()
Session = scoped_session(sessionmaker(autocommit=False, autoflush=False))
Base.query = Session.query_property()

#defining ModelBase
class ModelBase(Base):
    __abstract__ = True
    __tablename__ = ''

    def __init__(self, **kwargs):
        for key, value in list(kwargs.items()):
            if hasattr(self, key):
                self.__setattr__(key, value)

#defining the table
class cwt_bookings(ModelBase):
	__tablename__ = 'sia_app_db'

	id = Column(String, primary_key=True)
	created_on = Column(DateTime, nullable=False)
	updated_at = Column(DateTime)
	aircraft_reg_code = Column(String)
	aircraft_model = Column(String)
	flight_num = Column(String)
	origin = Column(String)
	departure_time = Column(DateTime)
	destination = Column(String)
	arrival_time = Column(DateTime)
	cabin_class = Column(String)
	seat_number = Column(String)
	problem_type = Column(String)
	problem_description = Column(String)
	priority = Column(String)
	status = Column(String)
	inventory = Column(String)

#creating the table
engine = get_engine()
Session.configure(bind=engine)
Base.metadata.create_all(engine)
print('table created')

# #foong connection
# db_conn_string = 'postgres://oehrcduj:AJu-p8-iNKeL5-qaPDL5EeA-E6CXVDyX@elmer.db.elephantsql.com:5432/oehrcduj'
# db_engine = create_engine(db_conn_string, connect_args={"application_name": "sia_app"})
# db_con = db_engine.raw_connection()

# #define insert function
# def insert_df(cls, df):
# 	csvf = csv.StringIO()
# 	df.to_csv(csvf, index=False, header=False, quotechar="'")
# 	csvf.seek(0)

# 	print('trying')
# 	con = get_connection()
# 	cur = con.cursor()
# 	cur.copy_from(csvf, 'sia_app_db', ',', columns=df.columns, null='')
# 	csvf.close()
# 	con.commit()
# 	con.close()	

# #insert dataframe into the table
# insert_df(db_con, final_insert_df)
# print("done!")