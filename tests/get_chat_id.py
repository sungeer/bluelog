import httpx


def get_chat_id(access_token, title):
    url = 'http://bebinca.cc/chat/chat-id'
    headers = {'Authorization': f'Bearer {access_token}'}
    data = {'title': title}
    with httpx.Client() as client:
        response = client.post(url, json=data, headers=headers)
        data = response.json()
        chat_id = data['data']
        return chat_id


if __name__ == '__main__':
    access_token = 'eyJhbGlWG13Nd84nNIY'
    title = '你是谁？'
    print(get_chat_id(access_token, title))
