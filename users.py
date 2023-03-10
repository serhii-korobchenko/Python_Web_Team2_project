
from db import db_session
import bcrypt
import models
import hashlib



def create_user(email, password, nick):
    hash = hashlib.sha256(password.encode('utf-8')).hexdigest()
    user = models.User(username=nick, email=email, hash=hash)
    db_session.add(user)
    db_session.commit()
    return user


def login(email, password):
    user = find_by_email(email)
    psw_hash = hashlib.sha256(password.encode('utf-8')).hexdigest()

    if not user:
        return None
    #if not bcrypt.checkpw(password.encode('utf-8'), user.hash):
    if not psw_hash == user.hash:
        return None
    return user


def find_by_email(email):
    user = db_session.query(models.User).filter(models.User.email == email).first()
    db_session.close()
    return user


def set_token(user, token):
    user.token_cookie = token
    db_session.commit()
    db_session.close()


def get_user_by_token(token):
    user = db_session.query(models.User).filter(models.User.token_cookie == token).first()
    if not user:
        return None
    return user
