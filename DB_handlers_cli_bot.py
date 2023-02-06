from sqlalchemy.engine import create_engine
from sqlalchemy.orm import sessionmaker, joinedload
from sqlalchemy.sql.operators import contains

from models import Email, Record, Adress, Phone, Birthday, Note, Tag
from sqlalchemy import and_, delete
from sqlalchemy.schema import MetaData
from sqlalchemy import or_
from flask import request, flash, redirect, render_template, url_for, Flask
from datetime import datetime, timedelta, date
from db import db_session

def birthday_in_days(number_days):

    checked_datetime = datetime.now() + timedelta(days=int(number_days))
    checked_date = checked_datetime.date()

    flag_birth = 0

    birthday_list = db_session.query(Birthday.birthday_date).all()

    for item in birthday_list:

        record_date = datetime(year=datetime.now().year, month=item[0].month,
                            day=item[0].day)


        if checked_date == record_date.date():
            rec_id = db_session.query(Birthday.rec_id).filter(Birthday.birthday_date == item[0]).first()
            name = db_session.query(Record.name).filter(Record.id == rec_id[0]).first()

            print(f' {name[0]} has birthday in {number_days} days! ')
            flash(f' {name[0]} has birthday in {number_days} days! ')
            flag_birth += 1

    if flag_birth == 0:
        print(f'No one  has birthday in {number_days} days!')
        flash(f'No one  has birthday in {number_days} days!')

def look_up_DB (text):

    global flag_lookup
    flag_lookup = 0

    query_list = [(Record.name, Record.id), (Record.created, Record.id), (Email.email_name, Email.rec_id),\
                  (Adress.adress_name, Adress.rec_id), (Phone.phone_name, Phone.rec_id)]
    for item in query_list:

        if db_session.query(item[0]).all():

            rec_id = db_session.query(item[1]).all()


            for outer in db_session.query(item[0], item[1]).all():

                if type(outer[0]) != str:
                    lookup_res = outer[0].strftime('%A %d %B %Y')
                else:
                    lookup_res = outer[0]

                if lookup_res.lower().find(text.lower()) >= 0:
                    print(
                        f'Looked up text was found in next statement: "{lookup_res}" in record: "{db_session.query(Record.name).filter(Record.id == outer[1]).first()[0]}"')
                    flash(
                        f'Looked up text was found in next statement: "{lookup_res}" in record: "{db_session.query(Record.name).filter(Record.id == outer[1]).first()[0]}"')

                    flag_lookup = 1

    if flag_lookup == 0:
        print(f'Unfortunately, Nothing was found. Sorry!')
        flash(f'Unfortunately, Nothing was found. Sorry!')

def add_records_DB(name, phone):
    phone1 = Phone(phone_name=phone)
    rec1 = Record(name=name, phones=[phone1])
    db_session.add(rec1)
    db_session.commit()


def change_phone_DB(name, new_phone):
    phone1 = db_session.query(Phone).filter(Phone.rec_id == str(db_session.query(Record.id).filter(Record.name == name).first()[0]))
    phone1.update({'phone_name': new_phone})
    db_session.commit()


def add_phone_DB(name, phone):
    phone1 = Phone(phone_name=phone, rec_id=str(db_session.query(Record.id).filter(Record.name == name).first()[0]))
    db_session.add(phone1)
    db_session.commit()


def del_phone_DB(name, phone):
    phone1 = db_session.query(Phone).filter(and_(Phone.phone_name == phone, Phone.rec_id==str(db_session.query(Record.id).filter(Record.name == name).first()[0])))
    phone1.delete()
    db_session.commit()


def del_rec_DB(name):
    rec_id = str(db_session.query(Record.id).filter(Record.name == name).one()[0])
    db_session.query(Phone).filter(Phone.rec_id==rec_id).delete()
    db_session.query(Email).filter(Email.rec_id == rec_id).delete()
    db_session.query(Adress).filter(Adress.rec_id == rec_id).delete()
    db_session.query(Record).filter(Record.name == name).delete()
    db_session.commit()


def add_email_DB(name, email):
    email1 = Email(email_name=email, rec_id=str(db_session.query(Record.id).filter(Record.name == name).first()[0]))
    db_session.add(email1)
    db_session.commit()


def change_email_DB(name, new_email):
    email1 = db_session.query(Email).filter(Email.rec_id == str(db_session.query(Record.id).filter(Record.name == name).first()[0]))
    email1.update({'email_name': new_email})
    db_session.commit()


def add_adress_DB(name, adress):
    adress1 = Adress(adress_name=adress, rec_id=str(db_session.query(Record.id).filter(Record.name == name).first()[0]))
    db_session.add(adress1)
    db_session.commit()


def change_adress_DB(name, new_adress):
    adress1 = db_session.query(Adress).filter(Adress.rec_id == str(db_session.query(Record.id).filter(Record.name == name).first()[0]))
    adress1.update({'adress_name': new_adress})
    db_session.commit()


def addnote_func_DB(title, text):
    note1 = Note(note_title=title, note_text=text)
    db_session.add(note1)
    db_session.commit()

def delnote_func_DB(title):
    note1 = db_session.query(Note).filter(Note.note_title == title)
    note1.delete()
    db_session.commit()








def addnote_func_DB(title, text):
    note1 = Note(note_title=title, note_text=text)
    db_session.add(note1)
    db_session.commit()

def delnote_func_DB(title):
    note1 = db_session.query(Note).filter(Note.note_title == title)
    note1.delete()
    db_session.commit()











def load_DB():
    records_DB = db_session.query(Record).all()

    DB_dict = {}
    for record in records_DB:
        record_dict = {
            'Name': record.name,
            'Phone': db_session.query(Phone.phone_name).filter(Phone.rec_id == record.id).all(),
            'Birthday': None,
            'Email': db_session.query(Email.email_name).filter(Email.rec_id == record.id).all(),
            'Adress': db_session.query(Adress.adress_name).filter(Adress.rec_id == record.id).all()
        }
        DB_dict[record.name] = record_dict

    return DB_dict

if __name__ == '__main__':
    # add_records_DB('Andrii', '888888888')
    # change_phone_DB('Bumba', '111111111')
    # add_phone_DB('Bumba', '2222222222')
    # del_phone_DB('Bumba', '2222222222')
    # del_rec_DB('Andrii')
    # add_email_DB('Bumba', '1@1.1')
    # change_email_DB('Bumba', '2@2.2')
    # add_adress_DB('Bumba', 'Vinica')
    # change_adress_DB('Bumba', 'Lviv')
    #look_up_DB ('11')
    res= load_DB()
    print(res)






