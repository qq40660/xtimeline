#!/usr/bin python
# -*- coding: utf-8 -*-
import sys

__author__ = 'Tony.Shao'

from xtimeline.models.database import WeiboAccounts
from xtimeline.helpers.weibo import friendships_create
from xtimeline.models.database import Users
from xtimeline.helpers import when
from xtimeline.helpers.storage import update_followers_count, store_friendships
from xtimeline.libs.weibo import APIError
#############################################################
import time
import traceback
import random


def creator():
    weibo_accounts = WeiboAccounts.query.filter(WeiboAccounts.status == 1, WeiboAccounts.friends_count < 1800,
                                                WeiboAccounts.expires_in > int(time.time())).all()
    for account in weibo_accounts:
        users = Users.query.filter(Users.followers_count >= 5000, Users.follower == 0).limit(5)
        for user in users:
            try:
                friendships_create(uid=user.uid, access_token=account.access_token, expires_in=account.expires_in)
                store_friendships(uid=account.uid, target_id=user.uid)
                update_followers_count(uid=account.uid)
                print account.uid, user.uid
            except APIError as e:
                #TODO User not exist
                # if e.error_code in [10013, 20003]:
                #     pass
                if e.error_code in [20506]:
                    if user.uid:
                        store_friendships(uid=account.uid, target_id=user.uid)
                        update_followers_count(uid=account.uid)
                        print account.uid, user.uid
                print traceback.format_exc()
            except Exception as e:
                print traceback.format_exc()
            finally:
                print '[CURRENT_TIME: %s]' % when.now()
                time.sleep(random.randint(10, 60))
                sys.stdout.flush()


def start():
    while True:
        creator()
        time.sleep(60 * 10)


if __name__ == '__main__':
    start()