import db
import models
import bcrypt


def create_user(email, password, nick):
    hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt(rounds=10))
    user = models.User(username=nick, email=email, hash=hash)
    db.db_session.add(user)
    db.db_session.commit()
    return user


def login(email, password):
    user = find_by_email(email)
    if not user:
        return None
    if not bcrypt.checkpw(password.encode('utf-8'), user.hash):
        return None
    return user


def find_by_email(email):
    user = db.db_session.query(models.User).filter(models.User.email == email).first()
    return user


def set_token(user, token):
    user.token_cookie = token
    db.db_session.commit()


def get_user_by_token(token):
    user = db.db_session.query(models.User).filter(models.User.token_cookie == token).first()
    if not user:
        return None
    return user
