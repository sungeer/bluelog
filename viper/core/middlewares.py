from starlette.requests import Request
from starlette.middleware import Middleware
from starlette.middleware.cors import CORSMiddleware
from starlette.middleware.authentication import AuthenticationMiddleware
from starlette.authentication import BaseUser, AuthCredentials, AuthenticationBackend

from viper.utils import jwt_util
from viper.models.user_model import UserModel

# cors
origins = [
    'http://127.0.0.1:8000',  # 后端应用使用的端口
    'http://127.0.0.1:8080',  # 前端应用使用的端口
]


# auth_required
class User(BaseUser):

    def __init__(self, user_id: int, username, phone):
        self.user_id = user_id
        self.username = username
        self.phone = phone

    @property
    def is_authenticated(self) -> bool:
        return True

    @property
    def display_name(self) -> str:
        return self.username


class JWTAuthBackend(AuthenticationBackend):

    async def authenticate(self, request: Request):
        if 'Authorization' not in request.headers:
            return None

        auth_header = request.headers['Authorization']
        try:
            scheme, token = auth_header.split()
            if scheme.lower() != 'bearer':
                return None
        except ValueError:
            return None

        user_id = jwt_util.verify_token(token)
        db_user = await UserModel().get_user_by_id(user_id)
        username = db_user['name']
        phone = db_user['phone']
        is_admin = db_user['is_admin']

        if is_admin:
            scopes = ['authenticated', 'admin']
        else:
            scopes = ['authenticated']

        return AuthCredentials(scopes), User(user_id, username, phone)


register_middlewares = [
    Middleware(
        CORSMiddleware,  # type: ignore
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=['*'],
        allow_headers=['*'],
    ),
    Middleware(
        AuthenticationMiddleware,  # type: ignore
        backend=JWTAuthBackend()
    ),
]
