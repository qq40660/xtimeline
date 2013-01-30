#!/usr/bin python
# -*- coding: utf-8 -*-
__author__ = 'Tony.Shao'

from xtimeline.config import MONGODB_HOST, MONGODB_PORT, MONGO_DB
from minimongo import Model, Index

class Statuses(Model):
    class Meta:
        host = MONGODB_HOST
        port = MONGODB_PORT
        database = MONGO_DB
        collection = 'statuses'
        indices = (
            Index("_id"),
            Index("uid"),
            Index("retweeted_status_id"),
            Index("created_at"),
            Index("reposts_count"),
            Index("comments_count")
            )


class Comments(Model):
    class Meta:
        host = MONGODB_HOST
        port = MONGODB_PORT
        database = MONGO_DB
        collection = 'comments'
        indices = (
            Index("_id"),
            Index("commented_status_id"),
            Index("created_at")
            )


class StatusesHistory(Model):
    class Meta:
        host = MONGODB_HOST
        port = MONGODB_PORT
        database = MONGO_DB
        collection = 'statuses_history'
        indices = (
            Index("id"),
            Index("created_at"),
            Index("reposts_count"),
            Index("comments_count")
            )


class RepostTimelineIDs(Model):
    class Meta:
        host = MONGODB_HOST
        port = MONGODB_PORT
        database = MONGO_DB
        collection = 'repost_timeline_ids'
        indices = (
            Index("wid"),
            Index([("wid", 1), ('retweeted_status_id', 1)], unique=True),
            Index("reposts_count"),
            Index("comments_count"),
            Index("created_at")
            )


class Users(Model):
    class Meta:
        host = MONGODB_HOST
        port = MONGODB_PORT
        database = MONGO_DB
        collection = 'users'
        indices = (
            Index("_id"),
            Index("verified"),
            Index("verified_type"),
            Index("friends_count"),
            Index("followers_count")
            )


class UsersHistory(Model):
    class Meta:
        host = MONGODB_HOST
        port = MONGODB_PORT
        database = MONGO_DB
        collection = 'users_history'
        indices = (
            Index("id"),
            Index("friends_count"),
            Index("followers_count")
            )

class Friendships(Model):
    class Meta:
        host = MONGODB_HOST
        port = MONGODB_PORT
        database = MONGO_DB
        collection = 'friendships'
        indices = (
            Index("_id"),
            Index([("uid", 1), ('follower_id', 1)], unique=True),
            Index("follower_id"),
            Index("status")
            )
