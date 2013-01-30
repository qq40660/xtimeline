#!/usr/bin python
# -*- coding: utf-8 -*-
from pymongo.errors import DuplicateKeyError

__author__ = 'Tony.Shao'

from xtimeline.models.database import WeiboAccounts
from xtimeline.helpers.weibo import friendships_create
from xtimeline.helpers.storage import store_friendships
from xtimeline.models.collections import Users
from xtimeline.libs.weibo import APIError
import time
import traceback


def start():
    weibo_accounts = WeiboAccounts.query.filter(WeiboAccounts.status == 1, WeiboAccounts.expires_in > int(time.time())).all()
    for account in weibo_accounts:
        try:
            users = Users.collection.find({'$or': [{'$gt': {'friends_count': 5000}},
                                                   {'verified': 1, '$gt': {'friends_count': 2000}}], 'followers': {'$ne': account.id}}).limit(5)
            for user in users:
                uid = user.id
                friendships_create(uid=uid, access_token=account.access_token, expires_in=account.expires_in)
                store_friendships(uid=uid, follower_id=account.id)
        except DuplicateKeyError as de:
            pass
        except APIError as ae:
            if ae.error_code in [10013, 20003]:
                pass
            print traceback.format_exc()
        except Exception as e:
            print traceback.format_exc()