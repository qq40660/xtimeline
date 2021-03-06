#!/usr/bin python
# -*- coding: utf-8 -*-
import traceback
from xtimeline.models.database import Statuses, Users, db_session, WeiboAccounts

__author__ = 'Tony.Shao'


def store_status(status, followers_count=0, db=1):  # 0 mysql 1 psql 2 mongo
    if status is None:
        return
    if status.get('deleted', 0):
        return
    document = Statuses.query.filter(Statuses.wid == status['wid']).first()
    if document:
        document.reposts_count = status['reposts_count']
        document.comments_count = status['comments_count']
        db_session.add(document)
        db_session.commit()
    else:
        if status.get('retweeted_status_id', 0):
            retweeted_status = Statuses.query.filter(Statuses.wid == status['retweeted_status_id']).first()
            if retweeted_status and followers_count >= 10000:
                retweeted_status.counter += 1
                db_session.add(retweeted_status)
        status = Statuses(**status)
        db_session.add(status)
        db_session.commit()


def store_user(user, db=1):
    if user is None:
        return
    document = Users.query.filter(Users.uid == user['uid']).first()
    if document:
        document.followers_count = user['followers_count']
        document.friends_count = user['friends_count']
        db_session.add(document)
        db_session.commit()
    else:
        user = Users(**user)
        db_session.add(user)
        db_session.commit()


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


def store_friendships(uid, target_id):
    Users.query.filter(Users.uid == target_id).update(
        {Users.follower: uid})
    db_session.commit()


def update_followers_count(uid):
    WeiboAccounts.query.filter(WeiboAccounts.uid == uid).update(
        {WeiboAccounts.friends_count: WeiboAccounts.friends_count + 1})
    db_session.commit()


def store_timeline(timeline):
    if timeline is None:
        return
    if not isinstance(timeline, list):
        raise TypeError('Need list')
    for status in timeline:
        try:
            if status.get('deleted', 0):
                continue
            user = status.pop('user', None)
            store_user(user) #保持用户信息
            store_status(status=status, followers_count=user['followers_count']) #保持微薄内容
            store_status_history(status) #保持微薄历史
            store_user_history(user) #保持用户历史
            retweeted_status = status.pop('retweeted_status', None)
            if retweeted_status:
                retweeted_status_user = retweeted_status.pop('user', None)
                store_user(retweeted_status_user) #保持用户信息
                store_status(retweeted_status) #保持微薄内容
                store_status_history(retweeted_status) #保持微薄历史
                store_user_history(retweeted_status_user) #保持用户历史
        except Exception:
            print traceback.format_exc()
    return len(timeline)


def get_user_account(access_token):
    account = WeiboAccounts.query.filter(WeiboAccounts.access_token == access_token).first()
    return account.uid, account.username, account.password


def update_access_token(uid, access_token, expires_in):
    WeiboAccounts.query.filter(WeiboAccounts.uid == uid).update(
        {WeiboAccounts.access_token: access_token, WeiboAccounts.expires_in: expires_in})
    db_session.commit()
