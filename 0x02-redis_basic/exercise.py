#!/usr/bin/env/python3

""" task 0"""

import redis
import uuid
from typing import Union


class Cache:
    """ Cache class with store method and create
    redis client"""
    def __init__(self) -> None:
        """ create redis client and flush database"""
        self._redis = redis.Redis()
        self._redis.flushdb()

    def store(data: Union[str, bytes, int, float]) -> str:
        """ store the input data with random key"""
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key
