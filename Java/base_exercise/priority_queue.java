import java.util.Collection;
import java.util.Collections;
import java.util.PriorityQueue;

/**
 * PriorityQueue 是 Java 标准库中基于二叉堆实现的 优先级队列。
 * 它默认是小顶堆（堆顶元素最小），如果需要大顶堆（堆顶元素最大），可以传入反序比较器。
 **/
public class priority_queue {

    public static void main(String[] args) {
        // 初始化优先队列，默认 小堆顶
        PriorityQueue<Object> minHeap = new PriorityQueue<>();

        // offer 添加元素
        minHeap.offer(30);
        minHeap.offer(10);
        minHeap.offer(20);

        // peek 获取堆顶元素(最小值)
        System.out.println(minHeap.peek());

        // poll 删除堆顶元素
        minHeap.poll();
        System.out.println(minHeap.peek());

        // size 获取堆的大小
        System.out.println(minHeap.size());

        // isEmpty 检查堆是否为空
        System.out.println(minHeap.isEmpty());

        /*
        * 大堆顶 传入反序比较器
        * */
        PriorityQueue<Object> maxHeap = new PriorityQueue<>(Collections.reverseOrder());
        maxHeap.offer(10);
        maxHeap.offer(30);
        maxHeap.offer(20);

        System.out.println(maxHeap.peek());
    }

}
