#!/usr/bin python
# -*- coding: utf-8 -*-
from xtimeline.helpers import when
from xtimeline.models.collections import Statuses, Users, Friendships

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


def store_timeline(timeline):
    if timeline is None:
        return
    if not isinstance(timeline, list):
        raise TypeError('Need list')
    for status in timeline:
        user = status.pop('user', None)
        store_user(user) #保持用户信息
        store_status(status) #保持微薄内容
        retweeted_status = status.pop('retweeted_status', None)
        if retweeted_status:
            user = retweeted_status.pop('user', None)
            store_user(user) #保持用户信息
            store_status(retweeted_status) #保持微薄内容
    return len(timeline)


def store_friendships(uid, target_id):
    friendship = Friendships(uid=uid, target_id=target_id, status=1, created_at = when.now())
    friendship.save()


def update_friendships_status(uid):
    Friendships.collection.update({'uid': uid}, {'$set': {'status': 0}}, multi=True)


if __name__ == '__main__':
    store_friendships(1, 1)

