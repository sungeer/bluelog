chat_id_schema = {
    'type': 'object',
    'properties': {
        'title': {
            'type': 'string',
            'minLength': 1,  # 不能为空字符串
            'maxLength': 20
        }
    },
    'required': ['title']  # 必填字段
}

send_message_schema = {
    'type': 'object',
    'properties': {
        'conversation_id': {
            'type': 'string',
            'minLength': 1
        },
        'content': {
            'type': 'string',
            'minLength': 1
        }
    },
    'required': ['conversation_id', 'content']
}

get_messages_schema = {
    'type': 'object',
    'properties': {
        'conversation_id': {
            'type': 'string',
            'minLength': 1
        }
    },
    'required': ['conversation_id']
}
