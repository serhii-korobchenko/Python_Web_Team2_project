from sqlalchemy import and_

import models, db
from libs.file_service import move_user_document, delete_user_file


def get_documents_user(user_id):
    return db.db_session.query(models.Document).filter(models.Document.user_id == user_id).all()


def get_document_user(doc_id, user_id):
    return db.db_session.query(models.Document).filter(
        and_(models.Document.user_id == user_id, models.Document.id == doc_id)).first()


def upload_file_for_user(user_id, file_path, description):
    new_filename, size = move_user_document(user_id, file_path)
    document = models.Document(description=description, user_id=user_id, path=new_filename, size=size)
    db.db_session.add(document)
    db.db_session.commit()


def update_document(doc_id, user_id, description):
    doc = get_document_user(doc_id, user_id)
    doc.description = description
    db.db_session.commit()


def delete_document_user(doc_id, user_id):
    delete_user_file(get_document_user(doc_id, user_id).path)
    db.db_session.query(models.Document).filter(
        and_(models.Document.user_id == user_id, models.Document.id == doc_id)).delete()
    db.db_session.commit()
