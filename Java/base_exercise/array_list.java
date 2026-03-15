import java.util.ArrayList;
import java.util.Collections;

/**
 * 动态数组 ArrayList 基础
 **/
public class array_list {

    public static void main(String[] args) {
        int n = 10;
        // 初始化 ArrayList，大小为 10，元素值都为 0
        // Collections.nCopies() -> List 极速克隆工具，用来创建一个包含 n 个相同对象引用 的列表
        ArrayList<Integer> nums = new ArrayList<>(Collections.nCopies(n, 0));
        // isEmpty 是否为空
        System.out.println(nums.isEmpty());
        // size 数组大小
        System.out.println(nums.size());
        // add 添加元素
        nums.add(20);
        System.out.println(nums.size());
        // get 获取元素
        System.out.println(nums.get(nums.size() - 1));
        // remove 删除元素
        nums.remove(nums.size()-1);
        System.out.println(nums.size());

        // set 修改索引上的元素
        nums.set(0, 39);
        System.out.println(nums.get(0));

        // add 指定位置插入元素
        nums.add(3,99);
        System.out.println(nums.get(3));

        // Collection交换元素
        Collections.swap(nums, 0,1);
        System.out.println(nums.get(0));

        System.out.println("------");
        //for 变量数组
        for (int num : nums){
            System.out.print(num + " ");
        }

    }

}
