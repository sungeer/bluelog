from utils import log
from models.user import User

import random


# 这个函数用来保存所有的 messages
message_list = []
session = {}


def random_str():
    seed = 'abcdefjsad89234hdsfkljasdkjghigaksldf89weru'
    s = ''
    for i in range(16):
        random_index = random.randint(0, len(seed) - 2)
        s += seed[random_index]
    return s


def template(name):
    """
    根据名字读取 templates 文件夹里的一个文件并返回
    """
    path = 'templates/' + name
    with open(path, 'r', encoding='utf-8') as f:
        return f.read()


def current_user(request):
    session_id = request.cookies.get('user', '')
    username = session.get(session_id, '游客')
    return username


def route_index(request):
    """
    主页的处理函数, 返回主页的响应
    """
    header = 'HTTP/1.1 210 VERY OK\r\nContent-Type: text/html\r\n'
    body = template('index.html')
    username = current_user(request)
    body = body.replace('{{username}}', username)
    r = header + '\r\n' + body
    return r.encode(encoding='utf-8')


def response_with_headers(headers):
    """
    Content-Type: text/html
    Set-Cookie: user=gua
    """
    header = 'HTTP/1.1 210 VERY OK\r\n'
    header += ''.join(['{}: {}\r\n'.format(k, v)
                           for k, v in headers.items()])
    return header


def route_login(request):
    """
    登录页面的路由函数
    """
    headers = {
        'Content-Type': 'text/html',
        # 'Set-Cookie': 'height=169; gua=1; pwd=2; Path=/',
    }
    # log('login, headers', request.headers)
    log('login, cookies', request.cookies)
    username = current_user(request)
    if request.method == 'POST':
        form = request.form()
        u = User(form)
        if u.validate_login():
            # session_id = random_str()
            # session[session_id] = u.username
            # headers['Set-Cookie'] = 'user={}'.format(session_id)
            user = User.find_by(username=u.username)
            session_id = random_str()
            session[session_id] = user.id
            headers['Set-Cookie'] = 'user={}'.format(session_id)
            # headers['Set-Cookie'] = 'user_id={}'.format(user.id)
            result = '登录成功'
            log('headers response', headers)
        else:
            result = '用户名或者密码错误'
    else:
        result = ''
    body = template('login.html')
    body = body.replace('{{result}}', result)
    body = body.replace('{{username}}', username)
    header = response_with_headers(headers)
    r = header + '\r\n' + body
    # log('login', r)
    return r.encode(encoding='utf-8')


def route_register(request):
    """
    注册页面的路由函数
    """
    header = 'HTTP/1.1 210 VERY OK\r\nContent-Type: text/html\r\n'
    if request.method == 'POST':
        form = request.form()
        u = User(form)
        if u.validate_register():
            u.save()
            result = '注册成功<br> <pre>{}</pre>'.format(User.all())
        else:
            result = '用户名或者密码长度必须大于2'
    else:
        result = ''
    body = template('register.html')
    body = body.replace('{{result}}', result)
    r = header + '\r\n' + body
    return r.encode(encoding='utf-8')


# def route_message(request):
#     """
#     消息页面的路由函数
#     """
#     log('本次请求的 method', request.method)
#     if request.method == 'POST':
#         form = request.form()
#         msg = Message(form)
#         log('post', form)
#         message_list.append(msg)
#         # 应该在这里保存 message_list
#     header = 'HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n'
#     # body = '<h1>消息版</h1>'
#     body = template('html_basic.html')
#     msgs = '<br>'.join([str(m) for m in message_list])
#     body = body.replace('{{messages}}', msgs)
#     r = header + '\r\n' + body
#     return r.encode(encoding='utf-8')


def route_profile(request):
    log('profile cookies', request.cookies)
    header = 'HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n'
    # body = '<h1>消息版</h1>'
    body = template('profile.html')
    session_id = request.cookies.get('user', '')
    user_id = session.get(session_id, -1)
    user = ''
    if user_id != -1:
        user = User.find_by(id=int(user_id))
    body = body.replace('{{user}}', str(user))
    r = header + '\r\n' + body
    return r.encode(encoding='utf-8')


def route_static(request):
    """
    静态资源的处理函数, 读取静态文件并生成响应返回
    """
    filename = request.query.get('file', )
    path = 'static/' + filename
    with open(path, 'rb') as f:
        header = b'HTTP/1.1 200 OK\r\n\r\n'
        img = header + f.read()
        return img


# 路由字典
# key 是路由(路由就是 path)
# value 是路由处理函数(就是响应)
route_dict = {
    '/': route_index,
    '/login': route_login,
    '/register': route_register,
    # '/messages': route_message,
    '/profile':route_profile,
}
