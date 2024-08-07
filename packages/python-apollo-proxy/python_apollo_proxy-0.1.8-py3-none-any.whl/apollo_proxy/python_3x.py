# -*- coding: utf-8 -*-
"""
# ---------------------------------------------------------------------------------------------------------
# ProjectName:  python-apollo
# FileName:     python_3x.py
# Description:  TODO
# Author:       GIGABYTE
# CreateDate:   2024/04/19
# Copyright ©2011-2024. Hunan xxxxxxx Company limited. All rights reserved.
# ---------------------------------------------------------------------------------------------------------
"""
import urllib.request
from urllib import parse
from .logger_handler import logger


def http_request(url, timeout, headers: dict = None):
    try:
        request = urllib.request.Request(url, headers=headers)
        res = urllib.request.urlopen(request, timeout=timeout)
        body = res.read().decode("utf-8")
        return res.code, body
    except Exception as e:
        if str(e).find("HTTP Error 304") != -1:
            return 304, dict()
        else:
            logger.error("http_request error, msg is %s", e)
            return 500, dict()


def url_encode(params):
    return parse.urlencode(params)
