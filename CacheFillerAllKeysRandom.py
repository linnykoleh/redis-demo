import redis
import random

def set_keys(redis_client, num_keys=10000):
    """Set keys without any expiration time."""
    for i in range(num_keys):
        key = f'key:{i}'
        value = f'value:{i}'
        redis_client.set(key, value)
        print(f"Set {key}")

if __name__ == "__main__":
    redis_client = redis.Redis(host='localhost', port=6379, password='yourmasterpassword')

    try:
        redis_client.ping()
        print("Connected to Redis!")

        # Step 1: Set keys
        set_keys(redis_client, num_keys=100000)

        print("Data insertion completed!")

    except redis.exceptions.ConnectionError as e:
        print(f"Could not connect to Redis: {e}")
