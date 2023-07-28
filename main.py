# -*- coding: utf-8 -*-

from scapy.all import *
import logging
from scapy.layers.inet import IP, TCP
import threading
import time

logging.getLogger('scapy.runtime').setLevel(logging.ERROR)

target_ip = '124.220.207.230'
target_port = 81
path = 'GET / HTTP/1.0 \r\n\r\n'

handshake_count = 0  # 握手成功计数器
lock = threading.Lock()  # 用于确保对计数器的线程安全操作


def start_tcp(target_ip, target_port):
    global handshake_count
    try:
        ans = sr1(IP(dst=target_ip) / TCP(dport=target_port, sport=RandShort(), seq=RandInt(), flags='S'),
                  verbose=False)
        if ans and TCP in ans:
            with lock:
                handshake_count += 1
            print('第一次握手成功！')
            print(ans[TCP])
            return True
        else:
            print('第一次握手失败！')
            return False
    except Exception as e:
        print('[-]有错误，请注意检查！')
        print("异常+e" + e)


def trans_data(target_ip, target_port, data):
    # 先建立TCP连接
    if start_tcp(target_ip, target_port):
       print("-------------------------------")
      


def write_stats():
    global handshake_count
    while True:
        time.sleep(60)  # 每隔十分执行一次写入操作

        with lock:
            count = handshake_count
            handshake_count = 0

        timestamp = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

        with open('handshake_stats.txt', 'a') as file:
            file.write('{}: 握手成功次数: {}\n'.format(timestamp, count))


if __name__ == '__main__':
    writer_thread = threading.Thread(target=write_stats)
    writer_thread.daemon = True  # 设置为守护线程，主线程退出时自动结束
    writer_thread.start()

    while True:
        t = threading.Thread(target=trans_data, args=(target_ip, target_port, path))
        t.start()
        t.join(0.1)
