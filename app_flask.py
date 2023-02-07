
from flask import Flask, render_template, request, redirect, flash, url_for
from models import Email, Record, Adress, Phone, Birthday, Note, Tag
from db import db_session
from Pekemons_IT_CLI_bot_with_SQLite import main, help_information
from datetime import datetime
from logging import DEBUG

app = Flask(__name__)
app.secret_key = b'pythonwebteam4'

app.debug = True
app.env = "development"
app.logger.setLevel(DEBUG)

class Record_Object:

    def __init__(self, name, phone, adress=None, email=None, birthday=None):
        self.name = name
        self.phone = phone
        self.adress = adress
        self.email = email
        self.birthday = birthday

class Note_Object:
    def __init__(self, note_title, note_text, created, tags=None):
        self.note_title = note_title
        self.note_text = note_text
        self.created = created
        self.tags = tags


@app.route("/", methods=['GET', 'POST'], strict_slashes=False)
def index():

    command = None

    if request.method == "POST":
        command = request.form.get("command")

        if 'addbirthday' in command:
            command_args = command.split(" ")
            messages = command_args[1]

            return redirect(url_for('add_birthday', messages=messages))

        else:
            main(command)

        return redirect("/")

    return render_template("index.html", help_information=help_information)

@app.route("/birthday/", methods=["GET", "POST"], strict_slashes=False)
def add_birthday():

    if request.method == "GET":
        messages = request.args['messages']
        global name_up
        name_up = messages

    else:
        name = name_up
        birthday_date_str = request.form.get("birthday_date")
        birthday_date = datetime.strptime(birthday_date_str, '%Y-%m-%d')
        print(f'TYPE OF birthday_date {type(birthday_date)}, RESULT = {birthday_date}')

        try:
            birthday_for_id = db_session.query(Birthday.birthday_date).filter(
                Birthday.rec_id == str(db_session.query(Record.id).filter(Record.name == name).first()[0])).all()
            print(birthday_for_id)
            if not birthday_for_id:
                birthday1 = Birthday(birthday_date=birthday_date,
                                    rec_id=str(db_session.query(Record.id).filter(Record.name == name).first()[0]))



                db_session.add(birthday1)
                db_session.commit()
                print('Birthday has been added successfully!')
                flash('Birthday has been added successfully!')

        except Exception as e:
            # flash (e.args)
            flash('Record with mentioned name does not exist. Try again!')

        return redirect("/")

    return render_template("add_birthday.html", messages=messages)

@app.route("/records_DB/", methods=["GET"], strict_slashes=False)
def data_base_rec():
    command = None
    records = db_session.query(Record).all()
    phones = db_session.query(Phone).all()

    record_list = []
    for record in records:
        record_id = record.id
        phone = db_session.query(Phone.phone_name).filter(Phone.rec_id == record.id).all() if db_session.query(Phone.phone_name).filter(Phone.rec_id == record.id).all() else '*'
        adress = db_session.query(Adress.adress_name).filter(Adress.rec_id == record.id).all() if db_session.query(Adress.adress_name).filter(Adress.rec_id == record.id).all() else '*'
        email = db_session.query(Email.email_name).filter(Email.rec_id == record.id).all() if db_session.query(Email.email_name).filter(Email.rec_id == record.id).all() else '*'
        birthday = db_session.query(Birthday.birthday_date).filter(Birthday.rec_id == record.id).all() if db_session.query(Birthday.birthday_date).filter(Birthday.rec_id == record.id).all() else '*'
        item_rec = Record_Object(record.name, phone, adress, email, birthday)
        item_rec.record_id = record_id
        record_list.append(item_rec)

    return render_template("data_base_rd.html", records=records, phones=phones, record_list=record_list)

@app.route("/notes_DB/", methods=["GET"], strict_slashes=False)
def data_base_notes():

    notes = db_session.query(Note).all()

    notes_list = []
    for note in notes:
        note_id = note.id
        tags = db_session.query(Tag.tag_text).filter(Tag.note_id == note.id).all() if db_session.query(Tag.tag_text).filter(Tag.note_id == note.id).all() else '*'
        item_note = Note_Object(note.note_title, note.note_text, note.created, tags)
        item_note.note_id = note_id

        notes_list.append(item_note)

    return render_template("data_base_nt.html",  notes_list=notes_list)



if __name__ == "__main__":
    app.run()
