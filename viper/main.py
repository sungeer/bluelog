from gevent import monkey

monkey.patch_all(thread=False, subprocess=False)

import sys
import socket
import time

import gevent
from gevent import socket

from viper.libs.request import Request


def parsed_path(path):
    query = {}
    # 'http://127.0.0.1:7788/abc?message=hello&author=gua'
    index = path.find('?')
    if index == -1:
        return path, query
    path, query_string = path.split('?', 1)
    args = query_string.split('&')
    for arg in args:
        k, v = arg.split('=')
        query[k] = v
    return path, query


def response_for_path(path, request):
    path, query = parsed_path(path)
    request.path = path
    request.query = query
    r = {
        '/static': route_static,
    }
    r.update(api_todo)
    r.update(user_routes)
    r.update(todo_routes)
    r.update(weibo_routes)
    #
    response = r.get(path, error)
    return response(request)


def handle_request(conn):
    try:
        while True:
            data = conn.recv(4096)
            if not data:
                break
            data = data.decode('utf-8')

            # 按 空行分割 header和body
            header_body = data.split('\r\n\r\n', 1)
            header_part = header_body[0]
            body_part = header_body[1] if len(header_body) > 1 else ''

            # 拆分 请求行 和每个 header
            lines = header_part.split('\r\n')
            request_line = lines[0]  # 请求行
            header_lines = lines[1:]  # 请求头行

            # 解析 请求行
            method, path, version = request_line.split(' ', 2)

            # 解析headers为字典
            headers = {}
            for line in header_lines:
                if ': ' in line:
                    key, value = line.split(': ', 1)
                    headers[key] = value

            request = Request()
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
