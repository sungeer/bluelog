import re

from jsonschema import validate, FormatChecker


# 自定义手机号码验证函数
def validate_phone_number(phone_number):
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
format_checker.checks('phone')(validate_phone_number)  # 注册 'phone' 格式验证
format_checker.checks('email')(validate_email)  # 注册 'email' 格式验证

# 定义 JSON Schema
schema = {
    'type': 'object',
    'properties': {
        'phone': {
            'type': 'string',
            'format': 'phone'  # 使用自定义的 'phone' 格式验证
        },
        'email': {
            'type': 'string',
            'format': 'email'  # 使用自定义的 'email' 格式验证
        }
    },
    'required': ['phone', 'email']  # 两个字段都是必填的
}

# 测试数据
data = {
    'phone': '13800138000',  # 有效的手机号码
    'email': 'test@example.com'  # 有效的邮箱地址
}

# data = {
#     'phone': '1234567890',  # 无效的手机号码
#     'email': 'invalid-email'  # 无效的邮箱地址
# }

# 验证数据
try:
    validate(instance=data, schema=schema, format_checker=format_checker)
    print('验证成功：数据是有效的手机号码和邮箱地址')
except Exception as e:
    print(f'验证失败：{e}')
