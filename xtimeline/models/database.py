#!/usr/bin python
# -*- coding: utf-8 -*-
__author__ = 'Tony.Shao'

from xtimeline.config import POSTGERSQL_DB_CONNECT_STRING, DB_SQL_ECHO
from xtimeline.helpers import when
from sqlalchemy import create_engine, Column
from sqlalchemy import INTEGER, VARCHAR, DATETIME, BIGINT
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

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
    created_at = Column(DATETIME, default=when.now)
    updated_at = Column(DATETIME, default=when.now, onupdate=when.now)


class Statuses(Model):
    __tablename__ = 'tb_weibo_statuses'
    pass

class Comments(Model):
    __tablename__ = 'tb_weibo_comments'
    pass

class StatusesHistory(Model):
    __tablename__ = 'tb_weibo_statuses_history'
    pass

class RepostTimelineIDs(Model):
    __tablename__ = 'tb_weibo_retweeted_timeline_ids'
    pass

class Users(Model):
    __tablename__ = 'tb_weibo_users'
    pass

class UsersHistory(Model):
    __tablename__ = 'tb_weibo_users_history'
    pass

class Friendships(Model):
    __tablename__ = 'tb_weibo_friendships'
    pass
