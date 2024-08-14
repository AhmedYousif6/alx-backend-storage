#!/usr/bin/env python3
"""implementing an expiring web cache and tracker"""

import redis
from functools import wraps
import requests


r = redis.Redis()


def url_access_count(method):
    """ decorator for get_page function"""
    @wraps(method)
    def wrapper(url):
        """ wrapper function"""
        key = "cache:" + url
        cached_value = r.get(key)
        if cached_value:
            return cached_value.decode("utf-8")
        key_count = "count:" + url
        html_content = method(url)
        r.incr(key_count)
        r.set(key, html_content, ex=10)
        r.expire(key, 10)
        return html_content
    return wrapper


@url_access_count
def get_page(url: str) -> str:
    """ optain the html content of a particular url"""
    result = requests.get(url)
    return result.text


if __name__ == "__main__":
    get_page("http://slowwly.robertomurray.co.uk")
