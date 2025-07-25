# uvicorn app:app

async def app(scope, receive, send):
    if scope['type'] == 'http':
        method = scope['method']  # 请求方法，如 'GET'
        path = scope['path']  # 路径，如 '/foo'
        query_string = scope['query_string'].decode()  # 查询字符串
        headers = {k.decode(): v.decode() for k, v in scope['headers']}  # headers 字典

        # 读取请求体
        body = b''
        while True:
            message = await receive()
            if message['type'] == 'http.request':
                body += message.get('body', b'')
                if not message.get('more_body', False):
                    break

        # 打印请求信息
        print(f'Method: {method}')
        print(f'Path: {path}')
        print(f'Query: {query_string}')
        print(f'Headers: {headers}')
        print(f'Body: {body.decode(errors="replace")}')

        # 响应
        await send({
            'type': 'http.response.start',
            'status': 200,
            'headers': [
                (b'content-type', b'text/plain; charset=utf-8'),
            ]
        })
        await send({
            'type': 'http.response.body',
            'body': b'Hello, ASGI!',
        })
