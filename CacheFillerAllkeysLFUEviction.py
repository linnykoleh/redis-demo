import redis
import random

def access_keys(redis_client, keys, num_accesses=10000):
    """Access some keys more frequently than others to test LFU eviction."""
    for _ in range(num_accesses):
        # Access a random key
        key = random.choice(keys)
        redis_client.get(key)

def fill_redis(redis_client, num_keys=1000):
    """Fill Redis with keys and values."""
    keys = []
    for i in range(num_keys):
        key = f'key:{i}'
        value = f'value:{i}'
        redis_client.set(key, value)
        keys.append(key)
    return keys

if __name__ == "__main__":
    redis_client = redis.Redis(host='localhost', port=6379, password='yourmasterpassword')

    try:
        redis_client.ping()
        print("Connected to Redis!")

        # Step 1: Fill Redis with data
        keys = fill_redis(redis_client, num_keys=10000)

        # Step 2: Simulate frequent access to some keys
        access_keys(redis_client, keys, num_accesses=100000)

        print("Data insertion and access simulation completed!")

    except redis.exceptions.ConnectionError as e:
        print(f"Could not connect to Redis: {e}")
