# -*- coding: utf-8 -*-
import sqlalchemy as sa

from data import db_session
from data.advertiser import Advertiser
from data.tasks import Task
from data.users import User


def is_introduced(user_id):
    db_sess = db_session.create_session()
    try:
        name = db_sess.query(User).filter(User.id == user_id).one().name
        return True
    except sa.exc.NoResultFound:
        return False


def introduce(message):
    user = User(
        id=message.chat.id,
        name=message.text)
    db_sess = db_session.create_session()
    db_sess.add(user)
    db_sess.commit()


def get_name(user_id):
    db_sess = db_session.create_session()
    name = db_sess.query(User).filter(User.id == user_id).one().name
    return name


def add_link_to_task(user_id, link):
    db_sess = db_session.create_session()
    user = db_sess.query(User).filter(User.id == user_id).one()
    task = Task(link=link)
    user.task = task
    db_sess.commit()


def add_action_to_task(user_id, action):
    db_sess = db_session.create_session()
    user = db_sess.query(User).filter(User.id == user_id).one()
    user.task.action = action
    db_sess.commit()


def take_data(user_id):
    db_sess = db_session.create_session()
    user = db_sess.query(User).filter(User.id == user_id).one()
    return user.name, user.task.link, user.task.action


def approve(user_id, status):
    db_sess = db_session.create_session()
    task = db_sess.query(User).filter(User.id == user_id).one().task
    task.approved = status
    db_sess.commit()


def is_approved(user_id):
    db_sess = db_session.create_session()
    task = db_sess.query(User).filter(User.id == user_id).one().task
    return task.approved


def get_user_id(username):
    db_sess = db_session.create_session()
    user_id = db_sess.query(User).filter(User.name == username).one().id
    return user_id


def is_registered(user_id):
    db_sess = db_session.create_session()
    try:
        db_sess.query(Advertiser).filter(Advertiser.id == user_id).one().name
    except sa.exc.NoResultFound:
        return False
    return True


def register(message):
    advertiser = Advertiser(
        id=message.chat.id,
        username=message.text)
    db_sess = db_session.create_session()
    db_sess.add(advertiser)
    db_sess.commit()


def get_task(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).filter(User.id == user_id).one().task


def get_all_advertisers_id():
    db_sess = db_session.create_session()
    return [_.id for _ in db_sess.query(Advertiser).all()]


def make_available(user_id):
    db_sess = db_session.create_session()
    advertiser = db_sess.query(Advertiser).filter(Advertiser.id == user_id).one()
    advertiser.available = True
    db_sess.commit()


def add_advertisers_to_task(user_id, advertisers):
    task = get_task(user_id)
    db_sess = db_session.create_session()
    task.advertisers
    [task.advertisers.append(ader) for ader in advertisers]
    db_sess.commit()
