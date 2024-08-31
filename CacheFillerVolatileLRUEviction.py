import redis
import time
import random

def set_keys_with_expiration(redis_client, num_keys=5000, ttl=60):
    """Set keys with an expiration time."""
    for i in range(num_keys):
        key = f'key:exp:{i}'
        value = f'value:{i}'
        redis_client.setex(key, ttl, value)  # setex sets the key with expiration
        print(f"Set {key} with expiration of {ttl} seconds")

def set_keys_without_expiration(redis_client, num_keys=5000):
    """Set keys without an expiration time."""
    for i in range(num_keys):
        key = f'key:noexp:{i}'
        value = f'value:{i}'
        redis_client.set(key, value)
        print(f"Set {key} without expiration")

if __name__ == "__main__":
    redis_client = redis.Redis(host='localhost', port=6379, password='yourmasterpassword')

    try:
        redis_client.ping()
        print("Connected to Redis!")

        # Step 1: Set keys with expiration
        set_keys_with_expiration(redis_client, num_keys=5000, ttl=80)

        # Step 2: Set keys without expiration
        set_keys_without_expiration(redis_client, num_keys=5000)

        print("Data insertion completed!")

    except redis.exceptions.ConnectionError as e:
        print(f"Could not connect to Redis: {e}")
