from starlette.routing import Router

from viper.views import chat_view

chat_url = Router()

chat_url.add_route('/chat-id', chat_view.get_chat_id, ['POST'])
chat_url.add_route('/send-message', chat_view.send_message, ['POST'])
chat_url.add_route('/chats', chat_view.get_chats, ['POST'])
chat_url.add_route('/messages', chat_view.get_messages, ['POST'])
