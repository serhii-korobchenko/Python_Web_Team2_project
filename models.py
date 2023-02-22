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

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String(120), nullable=False)
    email = Column(String(120), unique=True, nullable=False)
    hash = Column(String(255), nullable=False)
    token_cookie = Column(String(255), nullable=True, default=None)
    records = relationship('Record', back_populates='user')
    notes = relationship('Note', back_populates='user')
    pictures = relationship('Picture', back_populates='user')
    videos = relationship('Video', back_populates='user')
    documents = relationship('Document', back_populates='user')
    files = relationship('File', back_populates='user')
    # isDeleted = default False

    def __repr__(self):
        return f"User({self.id}, {self.username}, {self.email})"

# Таблица Record
class Record(Base):
    __tablename__ = "records"
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    created = Column(DateTime, default=datetime.now())
    emails = relationship("Email", cascade="all, delete", backref="records")
    adresses = relationship("Adress", cascade="all, delete",  backref="records")
    phones = relationship("Phone", cascade="all, delete",  backref="records")
    birthdays = relationship("Birthday", cascade="all, delete",  backref="records")
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    user = relationship('User', cascade='all, delete', back_populates='records')
    # phones = relationship("Phone",  secondary=record_m2m_phone, cascade="all, delete", backref="records")

# Таблица Email
class Email(Base):
    __tablename__ = "emails"
    id = Column(Integer, primary_key=True)
    email_name = Column(String(100), nullable=True)
    rec_id = Column(Integer, ForeignKey("records.id", ondelete="CASCADE"))
    user_id = Column(Integer, nullable=False)

# Таблица Adress
class Adress(Base):
    __tablename__ = "adresses"
    id = Column(Integer, primary_key=True)
    adress_name = Column(String(250), nullable=True)
    user_id = Column(Integer, nullable=False)
    rec_id = Column(Integer, ForeignKey("records.id", ondelete="CASCADE"))

# Таблица Phone
class Phone(Base):
    __tablename__ = "phones"
    id = Column(Integer, primary_key=True)
    phone_name = Column(String(20), nullable=True)
    user_id = Column(Integer, nullable=False)
    rec_id = Column(Integer, ForeignKey("records.id", ondelete="CASCADE"))


class Birthday(Base):
    __tablename__ = "birthdays"
    id = Column(Integer, primary_key=True)
    birthday_date = Column('birthday_date', DateTime, default=datetime.now())
    user_id = Column(Integer, nullable=False)
    rec_id = Column(Integer, ForeignKey("records.id", ondelete="CASCADE"))

class Note(Base):
    __tablename__ = "notes"
    id = Column(Integer, primary_key=True)
    note_title = Column(String(50), nullable=False)
    note_text = Column(String(250), nullable=False)
    created = Column(DateTime, default=datetime.now())
    tags = relationship("Tag", cascade="all, delete",  backref="notes")
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    user = relationship('User', cascade='all, delete', back_populates='notes')

class Tag(Base):
    __tablename__ = "tags"
    id = Column(Integer, primary_key=True)
    tag_text = Column(String(50), nullable=False)
    user_id = Column(Integer, nullable=False)
    note_id = Column(Integer, ForeignKey("notes.id", ondelete="cascade"))

class Picture(Base):
    __tablename__ = 'pictures'
    id = Column(Integer, primary_key=True)
    # uuid = db.Column()
    path = Column(String(350), unique=True,  nullable=False)
    description = Column(String(300), nullable=False)
    size = Column(Integer, nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    user = relationship('User', cascade='all, delete', back_populates='pictures')

    def __repr__(self):
        return f"Picture({self.id}, {self.path}, {self.size})"

class Video(Base):
    __tablename__ = 'videos'
    id = Column(Integer, primary_key=True)
    # uuid = db.Column()
    path = Column(String(350), unique=True,  nullable=False)
    description = Column(String(300), nullable=False)
    size = Column(Integer, nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    user = relationship('User', cascade='all, delete', back_populates='videos')

    def __repr__(self):
        return f"Video({self.id}, {self.path}, {self.size})"

class Document(Base):
    __tablename__ = 'documents'
    id = Column(Integer, primary_key=True)
    # uuid = db.Column()
    path = Column(String(350), unique=True,  nullable=False)
    description = Column(String(300), nullable=False)
    size = Column(Integer, nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    user = relationship('User', cascade='all, delete', back_populates='documents')

    def __repr__(self):
        return f"Document({self.id}, {self.path}, {self.size})"

class File(Base):
    __tablename__ = 'files'
    id = Column(Integer, primary_key=True)
    # uuid = db.Column()
    path = Column(String(350), unique=True,  nullable=False)
    description = Column(String(300), nullable=False)
    size = Column(Integer, nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    user = relationship('User', cascade='all, delete', back_populates='files')

    def __repr__(self):
        return f"File({self.id}, {self.path}, {self.size})"
#alembic revision --autogenerate -m 'Init'
#alembic upgrade head

if __name__ == "__main__":
    Base.metadata.create_all(engine)
