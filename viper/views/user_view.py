from viper.utils import jwt_util
from viper.utils.resp_util import jsonify, abort
from viper.models.user_model import UserModel
from viper.schemas import validator
from viper.schemas.user_schema import access_token_schema


async def get_access_token(request):
    body = await request.json()
    body = validator(body, access_token_schema)
    phone_number = body['phone_number']
    password = body['password']

    db_user = await UserModel().get_user_by_phone(phone_number)
    if not db_user:
        return abort(404, 'User not found')

    db_password = db_user['password_hash']
    is_pwd = jwt_util.validate_password(password, db_password)
    if not is_pwd:
        return abort(403, 'Incorrect password')

    user_id = db_user['id']
    access_token = jwt_util.generate_token({'id': user_id})
    jwt_token = {'access_token': access_token, 'token_type': 'bearer'}
    return jsonify(jwt_token)
