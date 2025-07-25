import asyncio


async def handle_http(reader, writer):
    """
    reader: asyncio.StreamReader 对象，用于异步读取客户端发来的数据
    writer: asyncio.StreamWriter 对象，用于异步写回数据给客户端
    """
    # 读取完整 HTTP 请求头
    data = b''
    while b'\r\n\r\n' not in data:
        chunk = await reader.read(4096)
        if not chunk:
            break
        data += chunk
        if len(data) > 8192:
            break  # 防止恶意包

    # 解析请求头
    try:
        header = data.decode(errors='replace')
        lines = header.split('\r\n')
        request_line = lines[0]
        method, path, _ = request_line.split()
        print(f'收到请求: {method} {path}')

        # 简单路由
        if path == '/':
            body = b'hello, world'
        elif path == '/ping':
            body = b'pong'
        else:
            body = b'404 not found'

        # 组装响应
        response = (
            'HTTP/1.1 200 OK\r\n'
            f'Content-Length: {len(body)}\r\n'
            'Content-Type: text/plain; charset=utf-8\r\n'
            'Connection: close\r\n'
            '\r\n'
        ).encode() + body

    except Exception as e:
        print('解析请求出错：', e)
        response = b'HTTP/1.1 400 Bad Request\r\nContent-Length: 11\r\n\r\nbad request'

    # 向客户端发送数据
    writer.write(response)  # 写入缓冲区
    await writer.drain()  # 把缓冲区数据发出去
    writer.close()
    await writer.wait_closed()


async def main():
    server = await asyncio.start_server(handle_http, '0.0.0.0', 8000)
    addr = server.sockets[0].getsockname()
    print(f'HTTP服务器运行中: http://{addr[0]}:{addr[1]}')
    async with server:
        await server.serve_forever()


asyncio.run(main())
