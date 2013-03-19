#!/usr/bin python
# -*- coding: utf-8 -*-
from xtimeline.models.database import Statuses, Users

__author__ = 'Tony.Shao'


def store_status(status, db=1):  # 0 mysql 1 psql 2 mongo
    if status is None:
        return
    document = Statuses.query.filter(Statuses.wid == status.wid).first()
    if document:
        status.id = document.id
        status.counter += 1
    status = Statuses(**status)
    status.save()


def store_user(user, db=1):
    if user is None:
        return
    document = Users.query.filter(Users.uid == user.uid).first()
    if document:
        user.id = document.id
    user = Users(**user)
    user.save()


def update_mongo_document(document, data):
    document = dict(document)
    document.update(data)
    return document


def store_status_history(status):
    """
    保持历史相关信息，转发评论数
    :param status:
    :return:
    """
    pass


def store_user_history(user):
    """
    保存历史相关，粉丝数等
    :param user:
    :return:
    """
    pass


def store_timeline(timeline):
    if timeline is None:
        return
    if not isinstance(timeline, list):
        raise TypeError('Need list')
    for status in timeline:
        user = status.pop('user', None)
        store_user(user) #保持用户信息
        store_status(status) #保持微薄内容
        store_status_history(status) #保持微薄历史
        store_user_history(user) #保持用户历史
        retweeted_status = status.pop('retweeted_status', None)
        if retweeted_status:
            retweeted_status_user = retweeted_status.pop('user', None)
            store_user(retweeted_status_user) #保持用户信息
            store_status(retweeted_status) #保持微薄内容
            store_status_history(retweeted_status) #保持微薄历史
            store_user_history(retweeted_status_user) #保持用户历史
    return len(timeline)

