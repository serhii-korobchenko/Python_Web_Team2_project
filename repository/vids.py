from sqlalchemy import and_

import models, db
from libs.file_service import move_user_video, delete_user_file


def get_videos_user(user_id):
    return db.db_session.query(models.Video).filter(models.Video.user_id == user_id).all()


def get_video_user(vid_id, user_id):
    return db.db_session.query(models.Video).filter(
        and_(models.Video.user_id == user_id, models.Video.id == vid_id)).first()


def upload_file_for_user(user_id, file_path, description):
    new_filename, size = move_user_video(user_id, file_path)
    video = models.Video(description=description, user_id=user_id, path=new_filename, size=size)
    db.db_session.add(video)
    db.db_session.commit()


def update_video(vid_id, user_id, description):
    vid = get_video_user(vid_id, user_id)
    vid.description = description
    db.db_session.commit()


def delete_video_user(vid_id, user_id):
    delete_user_file(get_video_user(vid_id, user_id).path)
    db.db_session.query(models.Video).filter(
        and_(models.Video.user_id == user_id, models.Video.id == vid_id)).delete()
    db.db_session.commit()
