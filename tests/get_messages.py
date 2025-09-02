import requests


def get_messages():
    url = 'http://127.0.0.1:8000/messages'
    data = {
        'content': '你好，这是一个测试消息',
        'sender': 'user'
    }

    response = requests.post(url, json=data)
    return response


if __name__ == '__main__':
    import time

    start_time = time.time()
    ret = get_messages()
    end_time = time.time()

    print('状态码：', ret.status_code)
    print('响应内容：', ret.text)

    elapsed_ms = (end_time - start_time) * 1000
    print('耗时：{:.2f} 毫秒'.format(elapsed_ms))
