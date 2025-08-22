import re

from jsonschema import validate, FormatChecker, ValidationError as ValidationException

from viper.utils.errors import ValidationError


# 自定义手机号码验证函数
def validate_phone(phone_number):
    pattern = r'^1[3-9]\d{9}$'
    if not re.match(pattern, phone_number):
        raise ValueError(f"'{phone_number}' 不是有效的手机号码")
    return True


# 自定义邮箱验证函数
def validate_email(email):
    pattern = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    if not re.match(pattern, email):
        raise ValueError(f"'{email}' 不是有效的邮箱地址")
    return True


# 注册自定义格式验证器
format_checker = FormatChecker()
format_checker.checks('phone')(validate_phone)  # 注册 'phone' 格式验证
format_checker.checks('email')(validate_email)  # 注册 'email' 格式验证


# 验证数据
def validator(data, schema, check_format=None):
    try:
        if check_format:
            validate(instance=data, schema=schema, format_checker=format_checker)
            return data
        validate(instance=data, schema=schema)
        return data
    except ValidationException as exc:
        raise ValidationError(exc.message)
