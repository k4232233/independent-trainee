import java.util.LinkedList;
import java.util.Queue;

/**
 * Queue 是 Java 标准库中的队列接口，常用的实现类有 LinkedList 和 PriorityQueue。
 **/
public class queue {

    public static void main(String[] args) {
        // 初始化一个空的整型队列 q
        Queue<Integer> q = new LinkedList<>();

        // offer 在队尾添加元素
        q.offer(10);
        q.offer(20);
        q.offer(30);

        //isEmpty 检查队列是否输出
        System.out.println(q.isEmpty());

        //size 获取队列的大小
        System.out.println(q.size());

        //获取队列的头元素
        System.out.println(q.peek());

        // 删除队列头元素
        q.poll();
        System.out.println(q.peek());
    }

}