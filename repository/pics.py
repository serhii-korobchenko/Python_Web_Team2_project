from sqlalchemy import and_

import models, db
from libs.file_service import move_user_picture, delete_user_file


def get_pictures_user(user_id):
    return db.db_session.query(models.Picture).filter(models.Picture.user_id == user_id).all()


def get_picture_user(pic_id, user_id):
    return db.db_session.query(models.Picture).filter(
        and_(models.Picture.user_id == user_id, models.Picture.id == pic_id)).first()


def upload_file_for_user(user_id, file_path, description):
    new_filename, size = move_user_picture(user_id, file_path)
    picture = models.Picture(description=description, user_id=user_id, path=new_filename, size=size)
    db.db_session.add(picture)
    db.db_session.commit()


def update_picture(pic_id, user_id, description):
    pic = get_picture_user(pic_id, user_id)
    pic.description = description
    db.db_session.commit()


def delete_picture_user(pic_id, user_id):
    delete_user_file(get_picture_user(pic_id, user_id).path)
    db.db_session.query(models.Picture).filter(
        and_(models.Picture.user_id == user_id, models.Picture.id == pic_id)).delete()
    db.db_session.commit()
