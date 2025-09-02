import requests
import threading

url = "http://127.0.0.1:8000/messages"
data = {
    "content": "你好，这是一个测试消息",
    "sender": "user"
}


def send_request(number):
    response = requests.post(url, json=data)
    print(f'线程{number} 状态码：{response.status_code} 响应内容：{response.text}')


# 配置并发数和请求总数
concurrent_num = 20  # 并发线程数
request_total = 100  # 请求总次数

threads = []
for i in range(request_total):
    t = threading.Thread(target=send_request, args=(i,))
    threads.append(t)
    t.start()
    if (i + 1) % concurrent_num == 0:
        for t in threads:
            t.join()
        threads = []

# 等待剩余线程
for t in threads:
    t.join()
