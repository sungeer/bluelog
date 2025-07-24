import json
from routes.session import session
from utils import (
    log,
    redirect,
    http_response,
    json_response,
)
from models.todo import Todo
from models.weibo import Weibo


def all_weibo(request):
    """
    返回所有 todo
    """
    ms = Weibo.all()
    # 要转换为 dict 格式才行
    data = [m.json() for m in ms]
    return json_response(data)


def add_weibo(request):
    """
    接受浏览器发过来的添加 weibo 请求
    添加数据并返回给浏览器
    """
    form = request.json()
    # 创建一个 model
    m = Weibo.new(form)
    # 把创建好的 model 返回给浏览器
    return json_response(m.json())


# 本文件只返回 json 格式的数据
# 而不是 html 格式的数据
def all(request):
    """
    返回所有 todo
    """
    todo_list = Todo.all()
    # 要转换为 dict 格式才行
    todos = [t.json() for t in todo_list]
    return json_response(todos)


def add(request):
    """
    接受浏览器发过来的添加 todo 请求
    添加数据并返回给浏览器
    """
    # 得到浏览器发送的 json 格式数据
    # 浏览器用 ajax 发送 json 格式的数据过来
    # 所以这里我们用新增加的 json 函数来获取格式化后的 json 数据
    form = request.json()
    # 创建一个 todo
    t = Todo.new(form)
    # 把创建好的 todo 返回给浏览器
    return json_response(t.json())


def delete(request):
    """
    通过下面这样的链接来删除一个 todo
    /delete?id=1
    """
    todo_id = int(request.query.get('id'))
    t = Todo.delete(todo_id)
    return json_response(t.json())


def update(request):
    form = request.json()
    todo_id = int(form.get('id'))
    t = Todo.update(todo_id, form)
    return json_response(t.json())


route_dict = {
    '/api/todo/all': all,
    '/api/todo/add': add,
    '/api/todo/delete': delete,
    '/api/todo/update': update,
    # weibo api
    '/api/weibo/all': all_weibo,
    '/api/weibo/add': add_weibo,

}
