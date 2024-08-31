# NoSQL Databases: Redis

## Build master-slave redis cluster.

```docker
version: '3.8'

services:
  redis-master:
    image: redis:latest
    container_name: redis-master
    ports:
      - "6379:6379"
    volumes:
      - ./conf/redis-master.conf:/usr/local/etc/redis/redis.conf
      - redis-master-data:/data
    command: redis-server /usr/local/etc/redis/redis.conf

  redis-slave-1:
    image: redis:latest
    container_name: redis-slave-1
    ports:
      - "6380:6379"
    volumes:
      - ./conf/redis-slave.conf:/usr/local/etc/redis/redis.conf
      - redis-slave-1-data:/data
    command: redis-server /usr/local/etc/redis/redis.conf
    depends_on:
      - redis-master

  redis-slave-2:
    image: redis:latest
    container_name: redis-slave-2
    ports:
      - "6381:6379"
    volumes:
      - ./conf/redis-slave.conf:/usr/local/etc/redis/redis.conf
      - redis-slave-2-data:/data
    command: redis-server /usr/local/etc/redis/redis.conf
    depends_on:
      - redis-master

volumes:
  redis-master-data:
  redis-slave-1-data:
  redis-slave-2-data:
```

## Try all eviction strategies.

### noeviction

To test the `noeviction` strategy, I generated a large number of keys and values in the Redis database.
I used a Python script ([CacheFillerNoEviction.py](CacheFillerNoEviction.py)) to generate the keys and values.
After inserting `67355` key when maxmemory is `1MB`, the Redis server stopped accepting new keys and values and I received the following error message:

```shell
  File "/Users/linnyk/IdeaProjects/LeetCoder/venv/lib/python3.11/site-packages/redis/client.py", line 565, in parse_response
    response = connection.read_response()
               ^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/linnyk/IdeaProjects/LeetCoder/venv/lib/python3.11/site-packages/redis/connection.py", line 536, in read_response
    raise response
redis.exceptions.OutOfMemoryError: command not allowed when used memory > 'maxmemory'.
```

### allkeys-lru

To test the `allkeys-lru` strategy, I generated a large number of keys and values in the Redis database.
I used a Python script ([CacheFillerAllkeysLRUEviction.py](CacheFillerAllkeysLRUEviction.py)) to generate the keys and values.
And `maxmemory 3mb`

![1.png](images/1.png)

![2.png](images/2.png)

```bash
localhost:6379> EXISTS key:712605
(integer) 0
```

and list resent key still in the cache.

```bash
localhost:6379> EXISTS key:999999
(integer) 1
```

### allkeys-lfu

To test the `allkeys-lfu` strategy,
I generated a number of keys and values in the Redis database and then did access to a random key.
I used a Python script ([CacheFillerAllkeysLFUEviction.py](CacheFillerAllkeysLFUEviction.py)) to generate the keys and values.
And `maxmemory 4mb`

![3.png](images/3.png)

### volatile-lru

To test the `volatile-lru` strategy,
I generated a number of `5000` key-value pair with `80` seconds ttl
and then again generated `5000` key-value pair but without ttl
I used a Python script ([CacheFillerVolatileLRUEviction.py](CacheFillerVolatileLRUEviction.py)) to generate the keys and values.
And `maxmemory 4mb`

#### This is a data in database right after insert `10000` records

![4.png](images/4.png)

![5.png](images/5.png)

### And this is after `80` seconds

![6.png](images/6.png)

![7.png](images/7.png)

### volatile-lfu

To test the `volatile-lfu` strategy,
I generated a number of `5000` key-value pair with `80` seconds ttl
and then again generated `5000` key-value pair but without ttl and then did random access to random key
I used a Python script ([CacheFillerVolatileLFUEviction.py](CacheFillerVolatileLFUEviction.py)) to generate the keys and values.
And `maxmemory 4mb`




