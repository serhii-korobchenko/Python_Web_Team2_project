from sqlalchemy import and_

import models, db
from libs.file_service import move_user_file, delete_user_file


def get_files_user(user_id):
    return db.db_session.query(models.File).filter(models.File.user_id == user_id).all()


def get_file_user(file_id, user_id):
    return db.db_session.query(models.File).filter(
        and_(models.File.user_id == user_id, models.File.id == file_id)).first()


def upload_file_for_user(user_id, file_path, description):
    new_filename, size = move_user_file(user_id, file_path)
    file = models.File(description=description, user_id=user_id, path=new_filename, size=size)
    db.db_session.add(file)
    db.db_session.commit()


def update_file(file_id, user_id, description):
    file = get_file_user(file_id, user_id)
    file.description = description
    db.db_session.commit()


def delete_file_user(file_id, user_id):
    delete_user_file(get_file_user(file_id, user_id).path)
    db.db_session.query(models.File).filter(
        and_(models.File.user_id == user_id, models.File.id == file_id)).delete()
    db.db_session.commit()
