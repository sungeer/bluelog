import httpx


def get_access_token(phone_number, password):
    url = 'http://127.0.0.1:8000/user/get-access-token'
    data = {
        'phone_number': phone_number,
        'password': password
    }
    with httpx.Client() as client:
        response = client.post(url, json=data)
        data = response.json()
        data_dict = data['data']
        access_token = data_dict['access_token']
        return access_token


if __name__ == '__main__':
    phone_number = ''
    password = ''
    access_token = get_access_token(phone_number, password)
    print(access_token)
