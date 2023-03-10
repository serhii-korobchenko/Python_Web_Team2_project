from sqlalchemy.engine import create_engine
from sqlalchemy.orm import sessionmaker, joinedload
from sqlalchemy.sql.operators import contains

from models import Email, Record, Adress, Phone, Birthday, Note, Tag, User
from sqlalchemy import and_, delete
from sqlalchemy.schema import MetaData
from sqlalchemy import or_, and_
from flask import request, flash, redirect, render_template, url_for, Flask, session
from datetime import datetime, timedelta, date
from db import db_session

def birthday_in_days(number_days):
    user_id = db_session.query(User.id).filter(User.username == list(session.values())[-1]["username"]).first()[0]

    checked_datetime = datetime.now() + timedelta(days=int(number_days))
    checked_date = checked_datetime.date()

    flag_birth = 0
    user_id = db_session.query(User.id).filter(User.username == list(session.values())[-1]["username"]).first()[0]
    list_rec_id = db_session.query(Record.id).filter(Record.user_id == user_id).all()
    list_rec_id_new = [item[0] for item in list_rec_id]

    birthday_list = []
    for item in list_rec_id_new:

        birthday = db_session.query(Birthday.birthday_date).filter(and_(Birthday.rec_id == item, Birthday.user_id == user_id)).first()
        if birthday:
            birthday_list.append(birthday)

    for birthday in birthday_list:

        record_date = datetime(year=datetime.now().year, month=birthday[0].month,
                            day=birthday[0].day)


        if checked_date == record_date.date():
            rec_id = db_session.query(Birthday.rec_id).filter(Birthday.birthday_date == birthday[0]).first()
            name = db_session.query(Record.name).filter(Record.id == rec_id[0]).first()

            print(f' {name[0]} has birthday in {number_days} days! ')
            flash(f' {name[0]} has birthday in {number_days} days! ')
            flag_birth += 1
        else:
            pass

    if flag_birth == 0:
        print(f'No one  has birthday in {number_days} days!')
        flash(f'No one  has birthday in {number_days} days!')


    db_session.close()

def look_up_DB (text):

    global flag_lookup
    flag_lookup = 0

    user_id = db_session.query(User.id).filter(User.username == list(session.values())[-1]["username"]).first()[0]
    list_rec_id = db_session.query(Record.id).filter(Record.user_id == user_id).all()
    list_rec_id_new = [item[0] for item in list_rec_id]

    query_list = [(Record.name, Record.id), (Record.created, Record.id), (Email.email_name, Email.rec_id),\
                  (Adress.adress_name, Adress.rec_id), (Phone.phone_name, Phone.rec_id), \
                  (Birthday.birthday_date, Birthday.rec_id),\
                  (Note.note_title, Note.id), (Note.note_text, Note.id), (Note.created, Note.id)]

    for item in query_list:

        if db_session.query(item[0]).all():

            for outer in db_session.query(item[0], item[1]).all():

                if type(outer[0]) != str:
                    lookup_res = outer[0].strftime('%A %d %B %Y')

                else:
                    lookup_res = outer[0]

                if lookup_res.lower().find(text.lower()) >= 0:
                    note = db_session.query(Note).filter(Note.id == item[1]).first()
                    rec_id = db_session.query(item[1]).first()[0]
                    # print(f'_________________item[1]_________________{rec_id}')
                    # print(f'_________________list_rec_id_new_________________{list_rec_id_new}')
                    if item[1] == Note.id and note.user_id == user_id:

                        print(
                            f'Looked up text was found in next statement: "{lookup_res}" in Note: "{db_session.query(Note.note_title).filter(Note.id == outer[1]).first()[0]}"')
                        flash(
                            f'Looked up text was found in next statement: "{lookup_res}" in Note: "{db_session.query(Note.note_title).filter(Note.id == outer[1]).first()[0]}"')

                        flag_lookup = 1

                    elif rec_id in list_rec_id_new:

                        print(
                            f'Looked up text was found in next statement: "{lookup_res}" in record: "{db_session.query(Record.name).filter(Record.id == outer[1]).first()[0]}"')
                        flash(
                            f'Looked up text was found in next statement: "{lookup_res}" in record: "{db_session.query(Record.name).filter(Record.id == outer[1]).first()[0]}"')

                        flag_lookup = 1

                    else:
                        pass

    if flag_lookup == 0:
        print(f'Unfortunately, Nothing was found. Sorry!')
        flash(f'Unfortunately, Nothing was found. Sorry!')

    db_session.close()

def findbytag_func_DB(tag): ####################################################

    global flag_findtag
    try:
        user_id = db_session.query(User.id).filter(User.username == list(session.values())[-1]["username"]).first()[0]
        flag_findtag = 0
        noteid_bytag = db_session.query(Tag.note_id).filter(and_(Tag.tag_text == tag, Tag.user_id == user_id)).first()[0]
        print(f'____________________________________{noteid_bytag}')
        found_note = db_session.query(Note.note_title).filter(Note.id == noteid_bytag).first()[0]


        print(f'{tag} was found in note with title:{found_note}')
        flash(f'{tag} was found in note with title:{found_note}')

    except:

        print(f'Unfortunately, Nothing was found. Sorry!')
        flash(f'Unfortunately, Nothing was found. Sorry!')

    db_session.close()

def add_records_DB(name, phone):
    user_id = db_session.query(User.id).filter(User.username == list(session.values())[-1]["username"]).first()[0]
    phone1 = Phone(phone_name=phone, user_id=user_id)
    rec1 = Record(name=name, phones=[phone1])
    # extract user from session
    rec1.user_id = user_id
    db_session.add(rec1)
    db_session.commit()
    db_session.close()


def change_phone_DB(name, new_phone):
    phone1 = db_session.query(Phone).filter(Phone.rec_id == str(db_session.query(Record.id).filter(Record.name == name).first()[0]))
    phone1.update({'phone_name': new_phone})
    db_session.commit()
    db_session.close()


def add_phone_DB(name, phone):
    user_id = db_session.query(User.id).filter(User.username == list(session.values())[-1]["username"]).first()[0]
    phone1 = Phone(phone_name=phone, rec_id=str(db_session.query(Record.id).filter(Record.name == name).first()[0]), user_id = user_id)
    db_session.add(phone1)
    db_session.commit()
    db_session.close()


def del_phone_DB(name, phone):
    user_id = db_session.query(User.id).filter(User.username == list(session.values())[-1]["username"]).first()[0]

    phone1 = db_session.query(Phone).filter(and_(Phone.phone_name == phone, Phone.rec_id==str(db_session.query(Record.id).filter(and_(Record.name == name, Record.user_id == user_id)).first()[0]), Phone.user_id == user_id))

    try:
        if db_session.query(Phone).filter(and_(Phone.phone_name == phone, Phone.rec_id==str(db_session.query(Record.id).filter(and_(Record.name == name, Record.user_id == user_id)).first()[0]), Phone.user_id == user_id)).one():
            phone1.delete()
            db_session.commit()
            db_session.close()
    except:
        raise ValueError




def del_rec_DB(name):
    rec_id = str(db_session.query(Record.id).filter(Record.name == name).one()[0])
    db_session.query(Phone).filter(Phone.rec_id==rec_id).delete()
    db_session.query(Email).filter(Email.rec_id == rec_id).delete()
    db_session.query(Adress).filter(Adress.rec_id == rec_id).delete()
    db_session.query(Birthday).filter(Birthday.rec_id == rec_id).delete()
    db_session.query(Record).filter(Record.name == name).delete()
    db_session.commit()
    db_session.close()


def add_email_DB(name, email):
    user_id = db_session.query(User.id).filter(User.username == list(session.values())[-1]["username"]).first()[0]
    email1 = Email(email_name=email, rec_id=str(db_session.query(Record.id).filter(Record.name == name).first()[0]), user_id=user_id)
    db_session.add(email1)
    db_session.commit()
    db_session.close()

def change_email_DB(name, new_email):
    email1 = db_session.query(Email).filter(Email.rec_id == str(db_session.query(Record.id).filter(Record.name == name).first()[0]))
    email1.update({'email_name': new_email})
    db_session.commit()
    db_session.close()

def add_adress_DB(name, adress):
    user_id = db_session.query(User.id).filter(User.username == list(session.values())[-1]["username"]).first()[0]
    adress1 = Adress(adress_name=adress, rec_id=str(db_session.query(Record.id).filter(Record.name == name).first()[0]), user_id=user_id)
    db_session.add(adress1)
    db_session.commit()
    db_session.close()


def change_adress_DB(name, new_adress):
    adress1 = db_session.query(Adress).filter(Adress.rec_id == str(db_session.query(Record.id).filter(Record.name == name).first()[0]))
    adress1.update({'adress_name': new_adress})
    db_session.commit()
    db_session.close()


def delbirthday_func_DB(name):
    birthday1 = db_session.query(Birthday).filter(Birthday.rec_id==str(db_session.query(Record.id).filter(Record.name == name).first()[0]))
    birthday1.delete()
    db_session.commit()
    db_session.close()


def addnote_func_DB(title, text):
    note1 = Note(note_title=title, note_text=text)
    note1.user_id = db_session.query(User.id).filter(User.username == list(session.values())[-1]["username"]).first()[0]
    db_session.add(note1)
    db_session.commit()
    db_session.close()

def delnote_func_DB(title):
    note_id = str(db_session.query(Note.id).filter(Note.note_title == title).one()[0])
    note1 = db_session.query(Note).filter(Note.note_title == title)
    db_session.query(Tag).filter(Tag.note_id == note_id).delete()
    note1.delete()
    db_session.commit()
    db_session.close()

def addtag_func_DB(tag_text, note):
    user_id = db_session.query(User.id).filter(User.username == list(session.values())[-1]["username"]).first()[0]
    note_id = db_session.query(Note.id).filter(and_(Note.note_title == note, Note.user_id == user_id)).first()[0]
    tag1 = Tag(tag_text=tag_text, note_id=str(note_id), user_id = user_id)
    db_session.add(tag1)
    db_session.commit()
    db_session.close()

def deltag_func_DB(tag_text):
    tag1 = db_session.query(Tag).filter(Tag.tag_text == tag_text)
    tag1.delete()
    db_session.commit()
    db_session.close()

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

    db_session.close()
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






