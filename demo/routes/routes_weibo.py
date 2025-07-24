from models.user import User
from models.weibo import Weibo
from models.weibo import Comment

from routes.session import session
from utils import (
    template,
    response_with_headers,
    http_response,
    redirect,
    error,
    log,
)

Tweet = Weibo


def current_user(request):
    session_id = request.cookies.get('user', '')
    user_id = session.get(session_id, -1)
    return user_id

# 微博相关页面
def index(request):
    body = template('weibo_index.html')
    return http_response(body)


route_dict = {
    '/weibo/index': index,
}
