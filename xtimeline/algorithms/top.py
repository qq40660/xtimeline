#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'Tony.Shao'


def hot(reposts_count, comments_count, created_at, weight=1):
    return reposts_count + comments_count + weight

def _calculate():
    pass