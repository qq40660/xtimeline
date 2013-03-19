#!/usr/bin python
# -*- coding: utf-8 -*-
__author__ = 'Tony.Shao'

import timelib
from xtimeline.helpers import when, base62


def sina_comments_parser(status):
    _status = dict()
    _status['id'] = status.id
    _status['current_id'] = status.id
    _status['_id'] = long(status.id)
    _status['text'] = status.text
    _status['status_type'] = 2
    _status['created_at'] = int(when.parse2Timestamp(timelib.strtodatetime(status.created_at)))
    _status_user = dict()
    _status_user['profile_image_url'] = status.user.profile_image_url
    _status_user['id'] = status.user.id
    _status_user['screen_name'] = status.user.screen_name
    _status_user['url'] = 'http://weibo.com/u/' + str(status.user.id)
    _status['user'] = _status_user
    commented_status = status.get('status', None)
    if commented_status:
        _commented_status = dict()
        if commented_status.get('deleted', None):
            _commented_status['id'] = commented_status.id
            _commented_status['_id'] = long(commented_status.id)
            _commented_status['text'] = commented_status.text
            _commented_status['deleted'] = 1
        else:
            _commented_status['id'] = commented_status.id
            _commented_status['_id'] = long(commented_status.id)
            _commented_status['text'] = commented_status.text
            _commented_status['created_at'] = int(
                when.parse2Timestamp(timelib.strtodatetime(commented_status.created_at)))
            _commented_status['url'] = 'http://weibo.com/' + str(
                commented_status.user.id) + '/' + base62.get_url(commented_status.mid)
            _commented_status['thumbnail_pic'] = commented_status.get('thumbnail_pic', '')
            _commented_status['bmiddle_pic'] = commented_status.get('bmiddle_pic', '')
            _commented_status['reposts_count'] = commented_status.get('reposts_count', 0)
            _commented_status['comments_count'] = commented_status.get('comments_count', 0)
            _commented_status_user = dict()
            _commented_status_user['profile_image_url'] = commented_status.user.profile_image_url
            _commented_status_user['id'] = commented_status.user.id
            _commented_status_user['screen_name'] = commented_status.user.screen_name
            _commented_status_user['url'] = 'http://weibo.com/' + str(commented_status.user.id)
            _commented_status['user'] = _commented_status_user
        _status['retweeted_status_id'] = _commented_status['_id']
        _status['retweeted_status'] = _commented_status

    reply_comment = status.get('reply_comment', None)
    if reply_comment:
        _reply_comment = dict()
        if _reply_comment.get('deleted', None):
            _reply_comment['id'] = reply_comment.id
            _reply_comment['_id'] = long(reply_comment.id)
            _reply_comment['text'] = reply_comment.text
            _reply_comment['deleted'] = 1
        else:
            _reply_comment['id'] = reply_comment.id
            _reply_comment['_id'] = long(reply_comment.id)
            _reply_comment['text'] = reply_comment.text
            _reply_comment['created_at'] = int(
                when.parse2Timestamp(timelib.strtodatetime(reply_comment.created_at)))
            _reply_comment_user = dict()
            _reply_comment_user['profile_image_url'] = reply_comment.user.profile_image_url
            _reply_comment_user['id'] = reply_comment.user.id
            _reply_comment_user['screen_name'] = reply_comment.user.screen_name
            _reply_comment_user['url'] = 'http://weibo.com/' + str(reply_comment.user.id)
            _reply_comment['user'] = _reply_comment_user
        _status['reply_comment'] = _reply_comment
        _status['reply_comment_id'] = _reply_comment['_id']

    return _status


def sina_homeline_parser(statuses):
    if statuses is None:
        return
    _statuses = []
    for status in statuses:
        _status = sina_status_parser(status)
        user = status.get('user', None)
        _user = sina_user_parser(user)
        if _user:
            _status['user'] = _user
            _status['uid'] = _user['uid']
        _status['retweeted_status_id'] = 0
        retweeted_status = status.get('retweeted_status', None)
        if retweeted_status:
            if retweeted_status.get('deleted', 0):
                _retweeted_status = sina_status_parser(retweeted_status)
            else:
                _retweeted_status = sina_status_parser(retweeted_status)
                retweeted_status_user = retweeted_status.get('user', None)
                _retweeted_status_user = sina_user_parser(retweeted_status_user)
                _retweeted_status['user'] = _retweeted_status_user
                _retweeted_status['uid'] = _retweeted_status_user['uid']
            _retweeted_status['retweeted_status_id'] = 0
            _status['retweeted_status_id'] = _retweeted_status['wid']
            _statuses.append(_retweeted_status)
        _statuses.append(_status)
    return _statuses


def sina_status_parser(status):
    if status is None:
        return
    _status = dict()
    if status.get('deleted', None):
        _status['wid'] = status['id']
        _status['deleted'] = 1
    else:
        _status['wid'] = status['id']
        _status['text'] = status['text']
        _status['created_at'] = timelib.strtodatetime(status['created_at'])
        _status['url'] = 'http://weibo.com/' + str(status['user']['id']) + '/' + base62.get_url(status['mid'])
        _status['original_pic'] = status.get('original_pic', '')
        _status['reposts_count'] = status.get('reposts_count', 0)
        _status['comments_count'] = status.get('comments_count', 0)
    return _status


def sina_user_parser(user):
    if user is None:
        return
    if user:
        status_user = {
            "uid": user['id'],
            "screen_name": user['screen_name'],
            "profile_image_url": user.get('profile_image_url', ''),
            "followers_count": user['followers_count'],
            "friends_count": user['friends_count'],
            "statuses_count": user['statuses_count'],
            "created_at": timelib.strtodatetime(user['created_at']),
            "verified": 1 if user.get('verified', 0) else 0,
            "verified_type": user.get('verified_type', 0),
            "gender": 1 if user.get('gender', 'm') == 'm' else 0,
            "verified_reason": user.get('verified_reason', '')
        }
        return status_user
