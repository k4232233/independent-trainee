import java.util.Arrays;
import java.util.LinkedList;

/**
 * 双链表 LinkedList 基础
 **/
public class linked_list {

    public static void main(String[] args) {
        LinkedList<Integer> lst = new LinkedList<>(Arrays.asList(1, 2, 3, 4, 5));

        // isEmpty 检测链表是否为空
        System.out.println(lst.isEmpty());

        // size 获取链表的大小
        System.out.println(lst.size());

        // addFirst 链表头部插入元素
        lst.addFirst(0);
        // addLast 链表尾部插入元素
        lst.addLast(6);

        // getFirst、getLast 获取首尾元素
        System.out.print(lst.getFirst() + " " + lst.getLast());

        // removeFirst 删除链表头部元素
        lst.removeFirst();
        // removeLast 删除链表尾部元素
        lst.removeLast();

        // 在链表中插入元素，并移动到第三个位置
        lst.add(2,99);

        // 删除链表中的某个元素
        lst.remove(2);

        System.out.println();
        System.out.println("-------");
        // 遍历链表
        for (int val : lst){
            System.out.print(val + " ");
        }
    }
}