#!/usr/bin python
# -*- coding: utf-8 -*-
__author__ = 'Tony.Shao'
import traceback
from xtimeline.helpers.statuses import sina_homeline_parser

from xtimeline.libs.weibo import APIClient
# from xtimeline.helpers import weibologin


def get_home_timeline(access_token, expires_in, since_id=0, max_id=0, count=100):
    """
    获取单账户的home_timeline，包括所有关注的账户发布信息
    """
    try:
        api = APIClient()
        api.set_access_token(access_token=access_token, expires=expires_in)
        if api.is_expires():
            error_message = '授权码过期，请重新授权！'
            #TODO 重新授权
            refresh_access_token()
            return
        if max_id > 0:
            max_id -= 1 # 偏移一个微薄
        resp = api.get.statuses__home_timeline(since_id=since_id, max_id=max_id, count=count)
        statuses = None
        if resp:
            statuses = resp.get('statuses', None)
        if statuses:
            _statuses = sina_homeline_parser(statuses)
            return _statuses
    except Exception:
        #TODO 异常处理
        print traceback.format_exc()


def get_statuses_counts(ids, access_token, expires_in):
    """
    批量获取转发评论数，新浪100个，id之间用逗号隔开
    """
    api = APIClient()
    api.set_access_token(access_token=access_token, expires=expires_in)
    resp = api.get.statuses__count(ids=ids)
    if api.is_expires():
        error_message = '授权码过期，请重新授权！'
        #TODO 重新授权
        refresh_access_token()
        return
    results = []
    for data in resp:
        result = {
            'id': data['id'],
            'comments_count': data['comments'],
            'reposts_count': data['reposts']
        }
        results.append(result)
    return results


def get_friendships_followers(uid, access_token, expires_in, count=200, cursor=0):
    """
    获取用户的粉丝列表
    """
    #TODO 未完成
    api = APIClient()
    api.set_access_token(access_token=access_token, expires=expires_in)
    resp = api.get.friendships__followers(uid=uid, count=200)
    if api.is_expires():
        error_message = '授权码过期，请重新授权！'
        #TODO 重新授权
        refresh_access_token()
        return
    results = []
    users = resp.users
    for user in users:
        result = {
            'id': users['id'],
            'comments_count': users['comments'],
            'reposts_count': users['reposts']
        }
        results.append(result)
    return results


def friendships_create(uid, access_token, expires_in):
    api = APIClient()
    api.set_access_token(access_token=access_token, expires=expires_in)
    if api.is_expires():
        error_message = '授权码过期，请重新授权！'
        #TODO 重新授权
        refresh_access_token()
        return False
    api.post.friendships__create(uid=uid)


def refresh_access_token():
    #TODO complete
    # weibologin.login(username, password)
    # access_token, expires_in = weibologin.getToken()
    pass