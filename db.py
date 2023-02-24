from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.engine import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
import psycopg2
import os
from env import main



#PostgreSQL database credentials for elephantsql
main()
user = os.environ.get('LOGIN')
password = os.environ.get('PASSWORD')


host = 'rogue.db.elephantsql.com'
port = '5432'
database = 'vtskvycg'

# create an engine to connect to the database
engine = create_engine(f'postgresql://{user}:{password}@{host}:{port}/{database}')


# #SQLite
# engine = create_engine(
#     "sqlite:///cli_bot.db", connect_args={"check_same_thread": False}, echo=True
# )

db_session = scoped_session(
    sessionmaker(autocommit=False, autoflush=False, bind=engine)
)

Base = declarative_base()