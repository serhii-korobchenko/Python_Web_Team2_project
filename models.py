from datetime import datetime
from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import ForeignKey, Table

from db import Base, engine, db_session

#таблица для связи many-to-many между таблицами records и email
record_m2m_phone = Table(
    "record_m2m_phone",
    Base.metadata,
    Column("id", Integer, primary_key=True),
    Column("record", Integer, ForeignKey("records.id")),
    Column("phone", Integer, ForeignKey("phones.id")),
)

# Таблица Record
class Record(Base):
    __tablename__ = "records"
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False, unique=True)
    created = Column(DateTime, default=datetime.now())
    emails = relationship("Email", cascade="all, delete", backref="records")
    adresses = relationship("Adress", cascade="all, delete",  backref="records")
    phones = relationship("Phone", cascade="all, delete",  backref="records")
    birthday = relationship("Birthday", cascade="all, delete",  backref="records")
    #phones = relationship("Phone",  secondary=record_m2m_phone, cascade="all, delete", backref="records")

# Таблица Email
class Email(Base):
    __tablename__ = "emails"
    id = Column(Integer, primary_key=True)
    email_name = Column(String(100), nullable=True)
    rec_id = Column(Integer, ForeignKey("records.id", ondelete="CASCADE"))

# Таблица Adress
class Adress(Base):
    __tablename__ = "adresses"
    id = Column(Integer, primary_key=True)
    adress_name = Column(String(250), nullable=True)
    rec_id = Column(Integer, ForeignKey("records.id", ondelete="CASCADE"))

# Таблица Phone
class Phone(Base):
    __tablename__ = "phones"
    id = Column(Integer, primary_key=True)
    phone_name = Column(String(20), nullable=True)
    rec_id = Column(Integer, ForeignKey("records.id", ondelete="cascade"))


class Birthday(Base):
    __tablename__ = "birthday"
    id = Column(Integer, primary_key=True)
    birthday_date = Column('birthday_date', DateTime, default=datetime.now())
    rec_id = Column(Integer, ForeignKey("records.id", ondelete="cascade"))





class Note(Base):
    __tablename__ = "notes"
    id = Column(Integer, primary_key=True)
    note_title = Column(String(50), nullable=False, unique=True)
    note_text = Column(String(250), nullable=False, unique=True)
    created = Column(DateTime, default=datetime.now())
    tags = relationship("Tag", cascade="all, delete",  backref="notes")

class Tag(Base):
    __tablename__ = "tags"
    id = Column(Integer, primary_key=True)
    tag_text = Column(String(50), nullable=False, unique=True)
    note_id = Column(Integer, ForeignKey("notes.id", ondelete="cascade"))

#alembic revision --autogenerate -m 'Init'
#alembic upgrade head

if __name__ == "__main__":
    Base.metadata.create_all(engine)
