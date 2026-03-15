"""
@Author：haoran.xu
"""
import asyncio
import time

# Ai常用知识点
# 知识点1. yield
"""
带有 yield 关键字的函数会变成一个生成器（Generator）
简单理解：会暂停的 Return
Java 中的 Stream

重点：按需生成，不占用额外内存。会自动保存所有局部变量和执行位置。
和传统的迭代器相比，逻辑写在一个连续的函数块里就行。

AI解释：可以随时暂停并记住现场的函数
"""


# 1. 控制台模拟
def simple_generator():
    print("--- 步骤 1：准备开始 ---")
    yield "第一条数据"
    time.sleep(1)

    print("--- 步骤 2：继续执行 ---")
    yield "第二条数据"
    time.sleep(1)

    print("--- 步骤 3：最后一步 ---")
    yield "第三条数据"
    time.sleep(1)


# 2. 模拟 Ai 吐字
def ai_response_simulator(text: str):
    words = text.split()
    for word in words:
        time.sleep(1)  # 阻塞的，模拟延时
        yield word  # 每次吐一个 chunk


# 3. 斐波那契
def fibonacci_generator():
    a, b = 0, 1
    while True:
        yield a  # 返回当前的数，并在此处暂停
        a, b = b, a + b  # 下次启动时执行，更新
        """
        提一嘴
        这是 Python 的 元组解构赋值，它会先计算右边的值再赋给左边
        so, 我们不需要定义中间变量 temp
        """


# 真是场景
"""
以上都是 yield 生成器同步版本，即会阻塞线程
下面介绍： 异步版，实际开发大都是用的异步
简单2步：
1. async 关键字修饰方法
2. 等待时，使用 asyncio.sleep()
"""


async def async_gen():
    for i in range(3):
        await asyncio.sleep(1)  # 非阻塞状态，等待时 CPU 可以去处理其他逻辑 / 请求
        yield f'Chunk {i}'


# 使用异步生成器
async def main():
    gen = simple_generator()
    print(f"接收到: {next(gen)}")
    print("（我是外部逻辑，我可以在两次 yield 之间做别的事）")
    print(f"接收到: {next(gen)}")
    print("（我是外部逻辑，我可以在两次 yield 之间做别的事）")
    print(f"接收到: {next(gen)}")
    print('*' * 10)

    print('Ai回答中：', end='', flush=True)
    """
    这里顺便说一下
    print 默认情况下，输出会先缓存在内存中，直到缓冲区满或程序结束才显示
    flush=True 强制立刻刷新缓冲区--即实时数据
    """
    for chunk in ai_response_simulator("你好! 我是 豆包， 很高兴 为你 服务"):
        print(chunk, end='', flush=True)
    print()
    print('*' * 10)

    fib = fibonacci_generator()
    for _ in range(10):
        print(next(fib), end=' ')
        """
        补充
        这里使用 _ 变量名
        告诉编译器，这个变量是多余的，我只是利用循环次数
        避免了变量被定义而未被使用
        """

    # 异步生成器的使用
    print("--- 开始获取数据 ---")
    # 注意必须使用 async for 和 async def
    async for c in async_gen():
        print(f"接收到： {c}")
    print("--获取结束--")


if __name__ == '__main__':
    print()
    print('*' * 10)
    asyncio.run(main())

"""
总结：
定义时：用 async def 和 yield
调用时：必须在 async def 函数内部用 async for
运行入口：用 asyncio.run() 启动
"""
