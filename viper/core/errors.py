from starlette.requests import Request
from starlette.exceptions import HTTPException, WebSocketException
from starlette.websockets import WebSocket

from viper.utils.log_util import logger
from viper.utils.resp_util import jsonify_exc
from viper.utils.errors import ValidationError, TokenExpiredError, AuthFailureError


async def validation_exception_handler(request: Request, exc: ValidationError):
    logger.opt(exception=True).warning(exc)
    return jsonify_exc(422, exc.message)


async def jwt_expired_exception_handler(request: Request, exc: TokenExpiredError):
    return jsonify_exc(401, exc.message)


async def jwt_failure_exception_handler(request: Request, exc: AuthFailureError):
    return jsonify_exc(400, exc.message)


async def http_exception_handler(request: Request, exc: HTTPException):
    logger.opt(exception=True).warning(exc)
    return jsonify_exc(exc.status_code, exc.detail)


async def global_exception_handler(request: Request, exc: Exception):
    logger.exception(exc)
    return jsonify_exc(500)


async def websocket_exception_handler(websocket: WebSocket, exc: WebSocketException):
    logger.opt(exception=True).warning(exc)
    await websocket.close(code=1008)


register_errors = {
    ValidationError: validation_exception_handler,
    TokenExpiredError: jwt_expired_exception_handler,
    AuthFailureError: jwt_failure_exception_handler,
    HTTPException: http_exception_handler,
    WebSocketException: websocket_exception_handler,
    Exception: global_exception_handler,
}
