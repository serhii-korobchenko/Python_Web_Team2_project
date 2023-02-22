
from flask import Flask, render_template, request, redirect, url_for, session, flash, make_response
from models import Email, Record, Adress, Phone, Birthday, Note, Tag, User
from db import db_session
from Pekemons_IT_CLI_bot_with_SQLite import main, help_information
from datetime import datetime
from logging import DEBUG
import users
from libs.validation_schemas import LoginSchema, RegistrationSchema
from marshmallow import ValidationError
from sqlalchemy.exc import IntegrityError
import uuid
from datetime import datetime, timedelta
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from libs.validation_file import doc, picture, video, allowed_file
from werkzeug.utils import secure_filename
import pathlib
from repository import users, pics, vids, docs, fls

app = Flask(__name__)
app.secret_key = b'pythonwebteam4'

app.debug = True
app.env = "development"
app.logger.setLevel(DEBUG)
# db = SQLAlchemy(app)
# migrate = Migrate(app, db)


class Record_Object:

    def __init__(self, name, phone, adress=None, email=None, birthday=None, user_id =None):
        self.name = name
        self.phone = phone
        self.adress = adress
        self.email = email
        self.birthday = birthday
        self.user_id = user_id

class Note_Object:
    def __init__(self, note_title, note_text, created, tags=None, user_id =None):
        self.note_title = note_title
        self.note_text = note_text
        self.created = created
        self.tags = tags
        self.user_id = user_id


@app.before_request
def before_func():
    auth = True if 'username' in session else False
    if not auth:
        token_user = request.cookies.get('username')
        if token_user:
            user = users.get_user_by_token(token_user)
            if user:
                session['username'] = {"username": user.username, "id": user.id}


@app.route('/healthcheck/', strict_slashes=False)
def healthcheck():
    return 'I am working'

#
# @app.route('/', strict_slashes=False)
# def index():
#     auth = True if 'username' in session else False
#     return render_template('index.html', title='Future is near!', auth=auth)


@app.route("/", methods=['GET', 'POST'], strict_slashes=False)
def bot():
    auth = True if 'username' in session else False
    command = None

    if request.method == "POST":
        command = request.form.get("command")

        if 'addbirthday' in command:
            command_args = command.split(" ")
            messages = command_args[1]

            return redirect(url_for('add_birthday', messages=messages))

        else:
            main(command)

        return redirect(url_for('bot'))

    if auth:
        values = list(session.values())
        username_session = values[-1]["username"]


        return render_template("bot1.html", help_information=help_information, auth=auth, title='Please sign in!', username_session = username_session)
    else:
        return render_template("bot1.html", help_information=help_information, auth=auth, title='Please sign in!')



@app.route('/registration/', methods=['GET', 'POST'], strict_slashes=False)
def registration():
    auth = True if 'username' in session else False
    if auth:
        return redirect(url_for('bot'))

    if request.method == 'POST':
        try:
            RegistrationSchema().load(request.form)
        except ValidationError as err:
            return render_template('registration.html', messages=err.messages)
        email = request.form.get('email')
        password = request.form.get('password')
        nick = request.form.get('nick')
        try:
            user = users.create_user(email, password, nick)
            print(user)
            return redirect(url_for('login'))
        except IntegrityError as err:
            print(err)
            return render_template('registration.html', messages={'error': f'User with email {email} exist!'})

    return render_template('registration.html')

@app.route('/login/', methods=['GET', 'POST'], strict_slashes=False)
def login():
    auth = True if 'username' in session else False
    if request.method == 'POST':
        try:
            LoginSchema().load(request.form)
        except ValidationError as err:
            return render_template('login.html', messages=err.messages)

        email = request.form.get('email')
        password = request.form.get('password')
        remember = True if request.form.get('remember') == 'on' else False

        user = users.login(email, password)
        if user is None:
            return render_template('login.html', messages={'err': 'Invalid credentials! Goto admin bro :)'})
        session['username'] = {"username": user.username, "id": user.id}
        response = make_response(redirect(url_for('bot')))
        if remember:
            # Треба створить token, та покласти його в cookie та БД
            token = str(uuid.uuid4())
            expire_data = datetime.now() + timedelta(days=60)
            response.set_cookie('username', token, expires=expire_data)
            users.set_token(user, token)

        return response
    if auth:
        return redirect(url_for('bot'))
    else:
        return render_template('login.html')


@app.route('/logout/', strict_slashes=False)
def logout():
    auth = True if 'username' in session else False
    if not auth:
        return redirect(request.url)  # Відправляє туди звідки він прийшов
    session.pop('username')
    response = make_response(redirect(url_for('bot')))
    response.set_cookie('username', '', expires=-1)

    return response


@app.route("/birthday/", methods=["GET", "POST"], strict_slashes=False)
def add_birthday():
    user_id = db_session.query(User.id).filter(User.username == list(session.values())[-1]["username"]).first()[0]
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
                                    rec_id=str(db_session.query(Record.id).filter(Record.name == name).first()[0]), user_id=user_id)

                db_session.add(birthday1)
                db_session.commit()
                print('Birthday has been added successfully!')
                flash('Birthday has been added successfully!')

        except Exception as e:
            # flash (e.args)
            flash('Record with mentioned name does not exist. Try again!')

        return redirect("/")

    db_session.close()
    return render_template("add_birthday.html", messages=messages)

@app.route("/records_DB/", methods=["GET"], strict_slashes=False)
def data_base_rec():
    command = None

    user_id = db_session.query(User.id).filter(User.username == list(session.values())[-1]["username"]).first()[0]
    user_name = list(session.values())[-1]["username"]
    records = db_session.query(Record).filter(Record.user_id == user_id).all()


    # phones = db_session.query(Phone).all()

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

    db_session.close()
    return render_template("data_base_rd.html", record_list=record_list, user_name = user_name)

@app.route("/notes_DB/", methods=["GET"], strict_slashes=False)
def data_base_notes():

    user_id = db_session.query(User.id).filter(User.username == list(session.values())[-1]["username"]).first()[0]
    user_name = list(session.values())[-1]["username"]
    notes = db_session.query(Note).filter(Note.user_id == user_id).all()

    notes_list = []
    for note in notes:
        note_id = note.id
        tags = db_session.query(Tag.tag_text).filter(Tag.note_id == note.id).all() if db_session.query(Tag.tag_text).filter(Tag.note_id == note.id).all() else '*'
        item_note = Note_Object(note.note_title, note.note_text, note.created, tags)
        item_note.note_id = note_id

        notes_list.append(item_note)

    db_session.close()
    return render_template("data_base_nt.html",  notes_list=notes_list, user_name = user_name)

@app.route("/pictures/upload/", methods=["GET", "POST"], strict_slashes=False)
def upload_pic():
    auth = True if 'username' in session else False
    if not auth:
        # return login()
        return redirect(request.url)
    if request.method == 'POST':
        description = request.form.get('description')
        if 'photo' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['photo']
        print(file)
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if  file or allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_path = pathlib.Path.cwd() /"uploads"/ filename
            file.save(file_path)

            if picture(file.filename):
                pics.upload_file_for_user(session['username']['id'], file_path, description)

            elif video(file.filename):
                vids.upload_file_for_user(session['username']['id'], file_path, description)

            elif doc(file.filename):
                docs.upload_file_for_user(session['username']['id'], file_path, description)

            else:
                fls.upload_file_for_user(session['username']['id'], file_path, description)

            flash('Uploaded successfully!')
            return redirect(url_for('upload_pic'))

    return render_template("upload_pic.html", auth=auth)

@app.route('/pictures', strict_slashes=False)
def pictures():
    auth = True if 'username' in session else False
    if not auth:
        return redirect(request.url)
    pictures_user = pics.get_pictures_user(session['username']['id'])
    return render_template('pictures.html', auth=auth, pictures=pictures_user)


@app.route('/pictures/edit/<pic_id>', methods=['GET', 'POST'], strict_slashes=False)
def pictures_edit(pic_id):
    auth = True if 'username' in session else False
    if not auth:
        return redirect(request.url)
    user_id = session['username']['id']
    picture = pics.get_picture_user(pic_id, user_id)
    if request.method == 'POST':
        description = request.form.get('description')
        pics.update_picture(pic_id, user_id, description)
        flash('Successfully!')
        return redirect(url_for('pictures'))

    return render_template('edit.html', auth=auth, picture=picture)


@app.route('/picture/delete/<pic_id>', methods=['POST'], strict_slashes=False)
def pictures_delete(pic_id):
    auth = True if 'username' in session else False
    if not auth:
        return redirect(request.url)
    user_id = session['username']['id']
    pics.delete_picture_user(pic_id, user_id)
    flash('Deleted successfully!')
    return redirect(url_for('pictures'))

@app.route('/videos', strict_slashes=False)
def videos():
    auth = True if 'username' in session else False
    if not auth:
        return redirect(request.url)
    videos_user = vids.get_videos_user(session['username']['id'])
    # print(videos_user)
    return render_template('videos.html', auth=auth, videos=videos_user)


@app.route('/videos/edit/<vid_id>', methods=['GET', 'POST'], strict_slashes=False)
def videos_edit(vid_id):
    auth = True if 'username' in session else False
    if not auth:
        return redirect(request.url)
    user_id = session['username']['id']
    video = vids.get_video_user(vid_id, user_id)
    if request.method == 'POST':
        description = request.form.get('description')
        vids.update_video(vid_id, user_id, description)
        flash('Successfully!')
        return redirect(url_for('videos'))

    return render_template('edit_video.html', auth=auth, video=video)


@app.route('/videos/delete/<vid_id>', methods=['POST'], strict_slashes=False)
def videos_delete(vid_id):
    auth = True if 'username' in session else False
    if not auth:
        return redirect(request.url)
    user_id = session['username']['id']
    vids.delete_video_user(vid_id, user_id)
    flash('Deleted successfully!')
    return redirect(url_for('videos'))


@app.route('/documents', strict_slashes=False)
def documents():
    auth = True if 'username' in session else False
    if not auth:
        return redirect(request.url)
    documents_user = docs.get_documents_user(session['username']['id'])
    print(documents_user)
    return render_template('documents.html', auth=auth, documents=documents_user)


@app.route('/document/edit/<doc_id>', methods=['GET', 'POST'], strict_slashes=False)
def document_edit(doc_id):
    auth = True if 'username' in session else False
    if not auth:
        return redirect(request.url)
    user_id = session['username']['id']
    document = docs.get_document_user(doc_id, user_id)
    if request.method == 'POST':
        description = request.form.get('description')
        docs.update_document(doc_id, user_id, description)
        flash('Successfully!')
        return redirect(url_for('documents'))

    return render_template('edit_document.html', auth=auth, document=document)


@app.route('/document/delete/<doc_id>', methods=['POST'], strict_slashes=False)
def document_delete(doc_id):
    auth = True if 'username' in session else False
    if not auth:
        return redirect(request.url)
    user_id = session['username']['id']
    docs.delete_document_user(doc_id, user_id)
    flash('Deleted successfully!')
    return redirect(url_for('documents'))

@app.route('/files', strict_slashes=False)
def files():
    auth = True if 'username' in session else False
    if not auth:
        return redirect(request.url)
    files_user = fls.get_files_user(session['username']['id'])
    print(files_user)
    return render_template('files.html', auth=auth, files=files_user)


@app.route('/file/edit/<file_id>', methods=['GET', 'POST'], strict_slashes=False)
def filet_edit(file_id):
    auth = True if 'username' in session else False
    if not auth:
        return redirect(request.url)
    user_id = session['username']['id']
    file = fls.get_file_user(file_id, user_id)
    if request.method == 'POST':
        description = request.form.get('description')
        fls.update_file(file_id, user_id, description)
        flash('Successfully!')
        return redirect(url_for('files'))

    return render_template('edit_file.html', auth=auth, file=file)


@app.route('/file/delete/<file_id>', methods=['POST'], strict_slashes=False)
def file_delete(file_id):
    auth = True if 'username' in session else False
    if not auth:
        return redirect(request.url)
    user_id = session['username']['id']
    fls.delete_file_user(file_id, user_id)
    flash('Deleted successfully!')
    return redirect(url_for('files'))


if __name__ == "__main__":
    app.run(host="localhost", port=8000, debug=True)
