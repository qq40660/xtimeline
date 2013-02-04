#!/usr/bin python
# -*- coding: utf-8 -*-

__author__ = 'Tony.Shao'

from xtimeline.models.database import WeiboAccounts
from xtimeline.helpers.weibo import friendships_create
from xtimeline.helpers.storage import store_friendships
from xtimeline.models.collections import Users
from xtimeline.libs.weibo import APIError
from pymongo.errors import DuplicateKeyError
#############################################################
import time
import traceback
import random


def start():
    weibo_accounts = WeiboAccounts.query.filter(WeiboAccounts.status == 1, WeiboAccounts.expires_in > int(time.time())).all()
    for account in weibo_accounts:
        uid = 0
        try:
            users = Users.collection.find({'$or': [{'friends_count': {'$gt': 5000}},
                                                   {'verified': True, 'friends_count': {'$gt': 2000}}], 'followers': {'$exists': False}}).limit(5)
            for user in users:
                uid = user.id
                print uid
                friendships_create(uid=uid, access_token=account.access_token, expires_in=account.expires_in)
                store_friendships(uid=uid, follower_id=account.uid)
                time.sleep(60 * random.randint(1, 10))
        except DuplicateKeyError as de:
            pass
        except APIError as ae:
            if ae.error_code in [10013, 20003]:
                pass
            if ae.error_code in [20506]:
                if uid:
                    store_friendships(uid=uid, follower_id=account.uid)
            print traceback.format_exc()
        except Exception as e:
            print traceback.format_exc()

if __name__ == '__main__':
    while True:
        start()
        time.sleep(60 * 10)