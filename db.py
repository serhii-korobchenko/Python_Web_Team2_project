from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.engine import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session


engine = create_engine(
    "sqlite:///cli_bot.db", connect_args={"check_same_thread": False}, echo=True
)

db_session = scoped_session(
    sessionmaker(autocommit=False, autoflush=False, bind=engine)
)

Base = declarative_base()