import redis

def set_keys_with_varying_ttl(redis_client, num_keys=5000):
    """Set keys with varying expiration times, ensuring TTL is always positive."""
    for i in range(num_keys):
        key = f'key:ttl:{i}'
        value = f'value:{i}'
        ttl = (i % 100) + 1  # Vary TTL between 1 and 100 seconds
        redis_client.setex(key, ttl, value)  # setex sets the key with expiration
        print(f"Set {key} with expiration of {ttl} seconds")

if __name__ == "__main__":
    redis_client = redis.Redis(host='localhost', port=6379, password='yourmasterpassword')

    try:
        redis_client.ping()
        print("Connected to Redis!")

        # Step 1: Set keys with varying TTL values
        set_keys_with_varying_ttl(redis_client, num_keys=5000)

        print("Data insertion completed!")

    except redis.exceptions.ConnectionError as e:
        print(f"Could not connect to Redis: {e}")
