from gevent import monkey

monkey.patch_all()

import sys
import socket
import time

import gevent
from gevent import socket


def handle_request(conn):
    try:
        while True:
            data = conn.recv(1024)
            data = data.decode('utf-8')
            print('收到的数据:', data)
            if len(data.split()) < 2:
                conn.close()
    except Exception as ex:
        print(ex)
    finally:
        conn.close()


def server(host='0.0.0.0', port=7788):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((host, port))
    s.listen(5)
    try:
        while True:
            conn, addr = s.accept()
            print(f'接收到来自客户端[{addr}]的数据')
            gevent.spawn(handle_request, conn)
    finally:
        s.close()


if __name__ == '__main__':
    server()
