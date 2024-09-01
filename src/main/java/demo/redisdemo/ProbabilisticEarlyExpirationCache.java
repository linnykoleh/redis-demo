package demo.redisdemo;

import redis.clients.jedis.Jedis;
import redis.clients.jedis.JedisClientConfig;

import java.util.Random;

public class ProbabilisticEarlyExpirationCache {
    private final Jedis jedis;
    private final double beta;
    private final Random random;

    public ProbabilisticEarlyExpirationCache(String host, int port, double beta) {
        jedis = new Jedis(host, port, new JedisClientConfig() {
            @Override
            public String getPassword() {
                return "yourmasterpassword";
            }
        });
        this.beta = beta;
        random = new Random();
    }

    public String fetch(String key, int ttl, CacheLoader loader) {
        var entry = cacheRead(key);
        var currentTime = System.currentTimeMillis();

        if (entry == null || shouldRecompute(entry, currentTime)) {
            var startTime = System.currentTimeMillis();
            var value = loader.load();
            var delta = System.currentTimeMillis() - startTime;

            cacheWrite(key, value, delta, ttl);
            return value;
        }

        return entry.getValue();
    }

    public void put(String key, String value, int ttl) {
        long delta = 0;  // Since we're directly writing, there's no computation time
        cacheWrite(key, value, delta, ttl);
    }

    private boolean shouldRecompute(CacheEntry entry, long currentTime) {
        var randomValue = random.nextDouble();
        var threshold = entry.getDelta() * beta * Math.log(randomValue);
        return (currentTime - threshold) >= entry.getExpiry();
    }

    private CacheEntry cacheRead(String key) {
        var value = jedis.get(key);
        var deltaStr = jedis.get(key + ":delta");
        var expiryStr = jedis.get(key + ":expiry");

        if (value == null || deltaStr == null || expiryStr == null) {
            return null;
        }

        var delta = Long.parseLong(deltaStr);
        var expiry = Long.parseLong(expiryStr);
        return new CacheEntry(value, delta, expiry);
    }

    private void cacheWrite(String key, String value, long delta, int ttl) {
        var expiryTime = System.currentTimeMillis() + ttl * 1000L;
        jedis.setex(key, ttl, value);
        jedis.setex(key + ":delta", ttl, String.valueOf(delta));
        jedis.setex(key + ":expiry", ttl, String.valueOf(expiryTime));
    }

    public void close() {
        if (jedis != null) {
            jedis.close();
        }
    }

    @FunctionalInterface
    public interface CacheLoader {
        String load();
    }

    private static class CacheEntry {
        private final String value;
        private final long delta;
        private final long expiry;

        public CacheEntry(String value, long delta, long expiry) {
            this.value = value;
            this.delta = delta;
            this.expiry = expiry;
        }

        public String getValue() {
            return value;
        }

        public long getDelta() {
            return delta;
        }

        public long getExpiry() {
            return expiry;
        }
    }
}
