from routes.session import session
from utils import (
    log,
    redirect,
    template,
    http_response,
)


def main_index(request):
    return redirect('/todo/index')


# 直接写函数名字不写 route 了
def index(request):
    """
    主页的处理函数, 返回主页的响应
    """
    body = template('todo_index.html')
    return http_response(body)


route_dict = {
    '/': main_index,
    '/todo/index': index,
}
