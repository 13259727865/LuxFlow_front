import time
import threading
from datetime import datetime


def thread2(para='hi'):
    """线程运行函数"""
    time.sleep(7)
    print(datetime.now())

    print(para)


def main():
    # 创建线程
    thread_hi = threading.Thread(target=thread2)
    thread_hello = threading.Thread(target=thread2, args=('hello',))
    # 启动线程
    thread_hi.start()
    thread_hello.start()
    print('Main thread has ended!')


if __name__ == '__main__':
    main()