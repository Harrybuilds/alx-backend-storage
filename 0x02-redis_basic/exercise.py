#!/usr/bin/env python3
"""
Cache class implementation with Redis storage.
"""
import redis
import uuid
from typing import Union, Optional, Callable
from functools import wraps


# Decorator to count the number of calls to a method
def count_call(method: Callable) -> Callable:
    @wraps(method)
    def wrapper(self, kwargs, args):
        # Increment the count for the method's qualified name
        self._redis.incr(method.__qualname__)
        # Call the original method
        return method(self, *args, **kwargs)
    return wrapper

# Decorator to store the input/output history of a method
def call_history(method: Callable) -> Callable:
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        # Generate Redis keys for storing inputs and outputs
        input_key = method.__qualname__ + ":inputs"
        output_key = method.__qualname__ + ":outputs"

        # Store the input arguments in the Redis list (as strings)
        self._redis.rpush(input_key, str(args))

        # Execute the original method and get the output
        output = method(self, *args, **kwargs)

        # Store the output in the Redis list
        self._redis.rpush(output_key, str(output))

        return output
    return wrapper

# Replay function to display the history of calls to a function
def replay(method: Callable) -> None:
    """Display the history of calls of a particular function."""
    redis_client = method.__self__._redis  # Access the Redis client from the method's instance
    method_name = method.__qualname__  # Get the method's qualified name

    input_key = method_name + ":inputs"
    output_key = method_name + ":outputs"

    # Get the number of calls by checking the length of the inputs list
    num_calls = redis_client.llen(input_key)

    # Print the number of calls
    print(f"{method_name} was called {num_calls} times:")

    # Retrieve the inputs and outputs
    inputs = redis_client.lrange(input_key, 0, -1)
    outputs = redis_client.lrange(output_key, 0, -1)

    # Print each input-output pair
    for input_args, output in zip(inputs, outputs):
        print(f"{method_name}(*{input_args.decode('utf-8')}) -> {output.decode('utf-8')}")


class Cache:
    def __init__(self):
        """Initialize the Cache and flush the Redis instance."""
        # Private Redis instance
        self._redis = redis.Redis()
        # Flush the Redis database
        self._redis.flushdb()

    @call_history  # Decorate store with call_history
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
