#!/usr/bin/env python3

""" advanced task """

import requests
import redis
import time
from typing import Callable
import functools


redis_client = redis.Redis()


def cache_with_expiration(expiration: int):
    """Decorator to cache the result of a function with an expiration time."""
    def decorator(func: Callable):
        """ decorator to cache"""
        @functools.wraps(func)
        def wrapper(url: str):
            """wrapper function"""
            cache_key = f"cache:{url}"

            cached_result = redis_client.get(cache_key)
            if cached_result:
                return cached_result.decode('utf-8')

            result = func(url)
            redis_client.setex(cache_key, expiration, result)
            return result

        return wrapper
    return decorator


def count_accesses(func: Callable):
    """Decorator to count the number of times a URL is accessed."""
    @functools.wraps(func)
    def wrapper(url: str):
        count_key = f"count:{url}"

        redis_client.incr(count_key)

        return func(url)

    return wrapper


@cache_with_expiration(expiration=10)
@count_accesses
def get_page(url: str) -> str:
    """Fetch the HTML content of the URL and return it."""
    response = requests.get(url)
    response.raise_for_status()
    return response.text
