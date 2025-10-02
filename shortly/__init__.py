from starlette.requests import Request

from shortly.core.routes import response_for_path


async def app(scope, receive, send):
    if scope['type'] == 'http':
        request = Request(scope, receive)
        method = request.method
        path = request.url.path
        query_string = str(request.url.query)
        headers = dict(request.headers)
        body = await request.body()  # body.decode(errors='replace')

        response = await response_for_path(request)
        await response(scope, receive, send)
    elif scope['type'] == 'websocket':
        # 1. 接受连接
        while True:
            message = await receive()
            if message['type'] == 'websocket.connect':
                # 允许连接
                await send({'type': 'websocket.accept'})
            elif message['type'] == 'websocket.receive':
                # 获取客户端发来的消息
                data = message.get('text') or message.get('bytes')
                print(f'WebSocket收到消息: {data}')

                # 回发消息给客户端
                await send({
                    'type': 'websocket.send',
                    'text': f'你发来: {data}'
                })
            elif message['type'] == 'websocket.disconnect':
                print('WebSocket断开')
                break
    if scope['type'] == 'lifespan':
        while True:
            message = await receive()
            if message['type'] == 'lifespan.startup':
                print('应用启动：初始化资源')
                # ...（初始化操作）
                await send({'type': 'lifespan.startup.complete'})
            elif message['type'] == 'lifespan.shutdown':
                print('应用关闭：释放资源')
                # ...（清理操作）
                await send({'type': 'lifespan.shutdown.complete'})
                break
