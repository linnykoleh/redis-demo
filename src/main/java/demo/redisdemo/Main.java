package demo.redisdemo;

public class Main {
    public static void main(String[] args) throws InterruptedException {
        var cache = new ProbabilisticEarlyExpirationCache("localhost", 6379, 1.0);

        cache.put("key1", "value1", 10);

        var value = cache.fetch("key1", 10, () -> {
            return "value2";
        });
        System.out.println("Value for key1: " + value); // Should print "value1"


        Thread.sleep(10000);
        value = cache.fetch("key1", 10, () -> {
            return "value2";
        });
        System.out.println("Value for key1: " + value); // Should print "value2"

        cache.close();
    }
}
