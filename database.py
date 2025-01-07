from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import MySQLdb

database_url = "mysql://Sudeshna:admin@localhost/rideshare_db"

# Create the database if it doesn't exist
def create_database():
    connection = MySQLdb.connect(host="localhost", user="Sudeshna", passwd="admin")
    cursor = connection.cursor()
    cursor.execute("CREATE DATABASE IF NOT EXISTS rideshare_db")
    cursor.close()
    connection.close()

create_database()

engine = create_engine(database_url)
Local_Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Create all tables
Base.metadata.create_all(bind=engine)