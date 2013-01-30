#!/usr/bin python
# -*- coding: utf-8 -*-
from pymongo.errors import DuplicateKeyError
from xtimeline.helpers import when
from xtimeline.models.collections import Statuses, Users, Friendships, RepostTimelineIDs

__author__ = 'Tony.Shao'

def store_status(status):
    if status is None:
        return
    if status.get('deleted', 0):
        stored_status = Statuses.collection.find_one(status['_id'])
        if stored_status:
            Statuses.collection.update({'_id': status['_id']}, {"$set": {'deleted': 1}})
        else:
            status = Statuses(**status)
            status.save()
    else:
        status = Statuses(**status)
        status.save()


def store_user(user):
    if user is None:
        return
    user = Users(**user)
    user.save()

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


def store_friendships(uid, follower_id):
    user = Users.collection.find_one(uid)
    if user:
        user.followers = follower_id
        user.save()
    friendship = Friendships(uid=uid, follower_id=follower_id, status=1, created_at = when.now())
    friendship.save()


def update_friendships_status(uid):
    Friendships.collection.update({'uid': uid}, {'$set': {'status': 0}}, multi=True)


def store_repost_timeline_ids(status_ids, retweeted_status_id):
    for status_id in status_ids:
        try:
            repost_timeline_ids = RepostTimelineIDs(wid=status_id, retweeted_status_id=retweeted_status_id)
            repost_timeline_ids.save()
        except DuplicateKeyError as pe:
            pass


if __name__ == '__main__':
    store_friendships(1, 1)

