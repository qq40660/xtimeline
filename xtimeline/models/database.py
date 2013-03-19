#!/usr/bin python
# -*- coding: utf-8 -*-
__author__ = 'Tony.Shao'

from sqlalchemy import create_engine, Column
from sqlalchemy import INTEGER, VARCHAR, DATETIME, BIGINT, TEXT
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from xtimeline.config import POSTGERSQL_DB_CONNECT_STRING, DB_SQL_ECHO
from xtimeline.helpers import when


def createEngine():
    engine = create_engine(POSTGERSQL_DB_CONNECT_STRING, convert_unicode=True, pool_recycle=3600, echo=DB_SQL_ECHO)
    return engine


engine = createEngine()
db_session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))
Model = declarative_base(name='Model')
Model.query = db_session.query_property()


class WeiboAccounts(Model):
    __tablename__ = 'tb_weibo_accounts'

    id = Column(INTEGER, primary_key=True)
    uid = Column(BIGINT)
    username = Column(VARCHAR(255))
    password = Column(VARCHAR(255))
    access_token = Column(VARCHAR(255))
    expires_in = Column(INTEGER)
    status = Column(INTEGER)
    friends_count = Column(INTEGER)
    created_at = Column(DATETIME, default=when.now)
    updated_at = Column(DATETIME, default=when.now, onupdate=when.now)


class Statuses(Model):
    __tablename__ = 'tb_weibo_statuses'

    id = Column(INTEGER, primary_key=True)
    wid = Column(BIGINT)
    uid = Column(BIGINT)
    retweeted_status_id = Column(BIGINT)
    text = Column(TEXT)
    original_pic = Column(VARCHAR(255))
    url = Column(VARCHAR(255))
    reposts_count = Column(INTEGER)
    comments_count = Column(INTEGER)
    counter = Column(INTEGER, default=1)  # counter
    created_at = Column(DATETIME, default=when.now)


class Users(Model):
    __tablename__ = 'tb_weibo_users'

    id = Column(INTEGER, primary_key=True)
    uid = Column(BIGINT)
    screen_name = Column(VARCHAR(255))
    profile_image_url = Column(VARCHAR(255))
    followers_count = Column(INTEGER)
    friends_count = Column(INTEGER)
    statuses_count = Column(INTEGER)
    verified = Column(INTEGER)
    verified_type = Column(INTEGER)
    verified_reason = Column(VARCHAR(255))
    gender = Column(INTEGER)
    follower = Column(BIGINT, default=0)
    created_at = Column(DATETIME, default=when.now)

