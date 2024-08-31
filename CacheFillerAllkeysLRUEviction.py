import redis
import random
import string

def generate_random_string(length=10):
    return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(length))

def fill_redis_data(redis_client, num_records=100000):
    for i in range(num_records):
        key = f'key:{i}'
        value = generate_random_string(50)
        redis_client.set(key, value)
        print(f"Set {key} -> {value}")

if __name__ == "__main__":
    redis_client = redis.Redis(
        host='localhost',
        port=6379,
        password='yourmasterpassword'
    )

    try:
        redis_client.ping()
        print("Connected to Redis!")

        fill_redis_data(redis_client, num_records=1000000)
        print("Data insertion completed!")

    except redis.exceptions.ConnectionError as e:
        print(f"Could not connect to Redis: {e}")
