import json

import httpx
from starlette.authentication import requires
from starlette.responses import StreamingResponse

from viper.core import settings
from viper.utils import tools, json_util
from viper.utils.http_util import httpx_common, httpx_stream
from viper.utils.resp_util import jsonify
from viper.utils.log_util import logger
from viper.models.chat_model import ChatModel
from viper.models.message_model import MessageModel
from viper.models.content_model import ContentModel
from viper.schemas import validator
from viper.schemas.chat_schema import chat_id_schema, send_message_schema, get_messages_schema

headers = {
    'Content-Type': 'application/json',
    'Access-key': settings.CONF.get_conf('AI', 'API_KEY'),
    'Workspace-Id': settings.CONF.get_conf('AI', 'WORKSPACE_ID')
}


@requires('authenticated')
async def get_chat_id(request):
    body = await request.json()
    body = validator(body, chat_id_schema)
    title = body['title']

    url = f'{settings.CONF.get_conf('AI', 'URL')}/v1/oapi/agent/chat/conversation/create'
    data = {
        'robot_id': settings.CONF.get_conf('AI', 'ROBOT_ID'),
        'user': 'wangxun',
        'title': title
    }
    response = await httpx_common.post(url, headers=headers, json=data)
    response = response.json()
    data = response.get('data')
    conversation_id = data.get('conversation_id')

    user = request.user
    user_id = user.id
    await ChatModel().add_chat(conversation_id, title, user_id)
    return jsonify(conversation_id)


async def get_response(conversation_id, content):
    url = f'{settings.CONF.get_conf('AI', 'URL')}/v1/oapi/agent/chat'
    data = {
        'robot_id': settings.CONF.get_conf('AI', 'ROBOT_ID'),
        'conversation_id': conversation_id,
        'content': content,
        'response_mode': 'streaming'
    }
    error_msg = {'finish': 'error'}
    try:
        async with httpx_stream.stream('POST', url=url, headers=headers, json=data) as response:
            async for line in response.aiter_lines():
                if not line:
                    continue
                yield line
    except httpx.TimeoutException:
        logger.error(f'ai time out: 【{conversation_id}】')
        yield f'data: {json_util.dict_to_json(error_msg)}\n\n'
    except (Exception,):
        logger.opt(exception=True).error(f'ai error 【{conversation_id}】.')
        yield f'data: {json_util.dict_to_json(error_msg)}\n\n'


async def stream_data(conversation_id, chat_id, trace_id, content):
    full_content = []
    async for line in get_response(conversation_id, content):
        answer = line.replace('data: ', '')
        try:
            answer = json_util.json_to_dict(answer)
        except json.JSONDecodeError:
            continue
        is_error = answer.get('finish')
        if is_error:
            yield f'{is_error}\n'
            break
        if answer.get('type') == 'TEXT' and answer.get('status') == 'SUCCEEDED':
            content = answer.get('content')
            full_content.append(content)
            yield f'{content}\n'

    content_str = ''.join(full_content) if full_content else 'error'
    message_id = await MessageModel().add_message(chat_id, trace_id, 'robot')
    await ContentModel().add_content(message_id, content_str)


@requires('authenticated')
async def send_message(request):
    body = await request.json()
    body = validator(body, send_message_schema)
    conversation_id = body['conversation_id']
    content = body['content']

    trace_id = tools.generate_random_id()
    chat_info = await ChatModel().get_chat_by_conversation(conversation_id)
    chat_id = chat_info['ID']

    message_id = await MessageModel().add_message(chat_id, trace_id, 'user')
    await ContentModel().add_content(message_id, content)

    return StreamingResponse(stream_data(conversation_id, chat_id, trace_id, content), media_type='text/event-stream')


# 所有会话
@requires('authenticated')
async def get_chats(request):
    user = request.user
    user_id = user.id
    chats = await ChatModel().get_chats(user_id)
    return jsonify(chats)


# 所有问答
@requires(['authenticated', 'admin'])
async def get_messages(request):
    body = await request.json()
    body = validator(body, get_messages_schema)
    conversation_id = body['conversation_id']

    chats = await MessageModel().get_messages(conversation_id)
    return jsonify(chats)
