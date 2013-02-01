#!/usr/bin python
# -*- coding: utf-8 -*-
__author__ = 'Tony.Shao'
import traceback
from xtimeline.helpers.statuses import sina_homeline_parser

from xtimeline.libs.weibo import APIClient

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
            return
        if max_id > 0:
            max_id -= 1 #偏移一个微薄
        resp = api.get.statuses__home_timeline(since_id=since_id, max_id=max_id, count=count)
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
    逗号分割，最多一百个
    :param ids:
    :param access_token:
    :param expires_in:
    :return:
    """
    api = APIClient()
    api.set_access_token(access_token=access_token, expires=expires_in)
    resp = api.get.statuses__count(ids=ids)
    results = []
    for data in resp:
        result = {
            'id': data['id'],
            'comments_count': data['comments'],
            'reposts_count': data['reposts']
        }
        results.append(result)
    return results


def friendships_create(uid, access_token, expires_in):
    api = APIClient()
    api.set_access_token(access_token=access_token, expires=expires_in)
    if api.is_expires():
        return
    api.get.friendships__create(uid=uid)


def get_repost_timeline_ids(wid, access_token, expires_in, since_id=0, count=200):

    api = APIClient()
    api.set_access_token(access_token=access_token, expires=expires_in)
    resp = api.get.statuses__repost_timeline__ids(id=wid,since_id=since_id)
    results = []
    status_ids = resp.get('statuses', None)
    for status_id in status_ids:
        result = {
            'wid': status_id,
            'retweeted_status_id': wid
        }
        results.append(result)
    return results