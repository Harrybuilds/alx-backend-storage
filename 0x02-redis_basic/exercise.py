#!/usr/bin/env python3
"""
Cache class implementation with Redis storage.
"""
import redis
import uuid
from typing import Union, Optional, Callable

class Cache:
    def __init__(self):
        """Initialize the Cache and flush the Redis instance."""
        # Private Redis instance
        self._redis = redis.Redis()
        # Flush the Redis database
        self._redis.flushdb()

    def store(self, data: Union[str, bytes, int, float]) -> str:
        """
        Store data in Redis with a random key.

        Args:
            data (Union[str, bytes, int, float]): The data to store.

        Returns:
            str: The generated key for the stored data.
        """
        # Generate a random UUID key
        key = str(uuid.uuid4())
        # Store data in Redis with the generated key
        self._redis.set(key, data)
        # Return the key
        return key

    def get(self, key: str, fn: Optional[callable] = None) -> Optional[Union[str, int, bytes]]:
        """
        Retrieve data from Redis, optionally
        using a callable function to convert the data.

        Args:
            key (str): The key to look up in Redis.
            fn (Callable, optional): A function to convert
            the retrieved data.

        Returns:
            Optional[Union[str, int, bytes]]: The retrieved
            data, optionally converted, or None if
            key does not exist.
        """

        value = self._redis.get(key)
        if value is None:
            return None

        # Apply the conversion function if provided
        if fn:
            fn(value)

        return value

    def get_str(self, key: str) -> Optional[str]:
        """
        Retrieve a value from Redis and decode it as a UTF-8 string.

        Args:
            key (str): The key to look up in Redis.

        Returns:
            Optional[str]: The decoded string, or None if the key doesn't exist.
        """
        return self.get(key, lambda d: d.decode("utf-8"))

    def get_int(self, key: str) -> Optional[int]:
        """
        Retrieve a value from Redis and convert it to an integer.

        Args:
            key (str): The key to look up in Redis.

        Returns:
            Optional[int]: The integer value, or None if the key doesn't exist.
        """
        return self.get(key, lambda d: int(d))