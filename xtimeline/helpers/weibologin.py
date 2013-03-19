#!/usr/bin/env python
# -*- coding: utf-8 -*-

import base64
import re
import json
import traceback
import time

import requests
from requests.compat import cookielib


APP_KEY = 3231340587
APP_SECRET = '94c4a0dc3c4a571b796ffddd09778cff'
CALLBACK_URL = 'http://2.xweiboproxy.sinaapp.com/callback.php'
RSA_SERVER_URL = 'http://localhost:8888/encrypt?password=%s'
session = requests.session()

postdata = {
    'entry': 'weibo',
    'gateway': '1',
    'savestate': '7',
    'userticket': '1',
    'vsnf': '1',
    'su': '',
    'service': 'miniblog',
    'servertime': '',
    'nonce': '',
    'pwencode': 'rsa2',
    'rsakv': '',
    'sp': '',
    'encoding': 'UTF-8',
    'pagerefer': '',
    'url': 'http://weibo.com/ajaxlogin.php?framelogin=1&callback=parent.sinaSSOController.feedBackUrlCallBack',
    'returntype': 'META'
}


def __get_servertime():
    '''
            获取服务器时间和nonce随机数
    '''
    url = 'http://login.sina.com.cn/sso/prelogin.php?entry=weibo&callback=sinaSSOController.preloginCallBack&su=&rsakt=mod&client=ssologin.js(v1.4.5)&_=1361178502112'
    data = requests.get(url).text
    p = re.compile('\((.*)\)')
    try:
        json_data = p.search(data).group(1)
        data = json.loads(json_data)
        servertime = str(data['servertime'])
        nonce = data['nonce']
        rsakv = data['rsakv']
        return servertime, nonce, rsakv
    except:
        print 'Get severtime error!'
        return None


def __get_pwd(pwd):
    '''
    RSA加密
    '''
    resp = session.get(RSA_SERVER_URL % pwd)
    return resp.content


def __get_user(username):
    '''
    username 经过了BASE64 计算
    '''
    username_ = requests.compat.quote(username)
    username = base64.encodestring(username_)[:-1]
    return username


def login(username, pwd):
    url = 'http://login.sina.com.cn/sso/login.php?client=ssologin.js(v1.4.5)'
    try:
        servertime, nonce, rsakv = __get_servertime()
    except Exception, e:
        print e
        return None
    postdata['servertime'] = servertime
    postdata['nonce'] = nonce
    postdata['su'] = __get_user(username)
    postdata['sp'] = __get_pwd(pwd)
    postdata['rsakv'] = rsakv
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.70 Safari/537.17'
    }

    result = session.post(
        url=url,
        data=postdata,
        headers=headers,
    )

    result.encoding = 'GBK'
    text = result.text
    print text
    p = re.compile('location\.replace\(\"(.*?)\"\)')

    try:
        # COOKIEJAR_CLASS = cookielib.LWPCookieJar
        # cookiejar = COOKIEJAR_CLASS('weibo_cookies')
        login_url = p.search(text).group(1)
        # session.get(login_url, cookies=cookiejar)
        session.get(login_url, allow_redirects=False)
        # cookiejar.save()
        print 'Login Success！'
        print session.get('http://www.weibo.com').text
    except Exception:
        print traceback.format_exc()
        return None


def getToken():
    authorize_url = "https://api.weibo.com/oauth2/authorize?client_id=%s&redirect_uri=%s&response_type=code" % (
        APP_KEY, CALLBACK_URL)
    print authorize_url
    response = session.get(authorize_url, allow_redirects=False)
    data = response.text
    print data
    token = data.get('access_token')
    expires_in = data.get('expires_in')
    if token:
        # expires等于当前时间加上有效期，单位为秒
        expires = int(expires_in[0]) + int(time.time())
        return token[0], expires


class WeiboError(StandardError):
    def __init__(self, error_code, error):
        self.error_code = error_code
        self.error = error
        StandardError.__init__(self, error)

    def __str__(self):
        return 'TokenGeneratorError: ErrorCode: %s, ErrorContent: %s' % (self.error_code, self.error)


if __name__ == '__main__':
    login('xeoncode@gmail.com', '299792458')
    getToken()