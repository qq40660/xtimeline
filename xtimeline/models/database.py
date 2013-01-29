#!/usr/bin python
# -*- coding: utf-8 -*-
__author__ = 'Tony.Shao'

from xtimeline.config import DB_CONNECT_STRING, DB_SQL_ECHO
from xtimeline.helpers import when
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column
from sqlalchemy.dialects.mysql import INTEGER, VARCHAR, DATETIME, BIGINT

def createEngine():
    engine = create_engine(DB_CONNECT_STRING, convert_unicode=True, pool_recycle=3600, echo=DB_SQL_ECHO)
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
