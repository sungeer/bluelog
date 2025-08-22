from base64 import b64encode, b64decode

from Crypto.Cipher import AES  # pip install pycryptodome
from Crypto.Util.Padding import pad, unpad

from viper.core import settings


class AESCipher:

    def __init__(self, key: str):
        key_hex = key
        key_bytes = bytes.fromhex(key_hex)
        if len(key_bytes) not in (16, 24, 32):
            raise ValueError('sec_key is error')
        self.key = key_bytes

    # 加密
    def encrypt(self, data):
        cipher = AES.new(self.key, AES.MODE_ECB)
        ct_bytes = cipher.encrypt(pad(data.encode(), AES.block_size))
        ct = b64encode(ct_bytes).decode('utf-8')
        return ct

    # 解密
    def decrypt(self, data):
        ct = b64decode(data)
        cipher = AES.new(self.key, AES.MODE_ECB)
        pt = unpad(cipher.decrypt(ct), AES.block_size)
        return pt.decode('utf-8')


secret_key = settings.CONF.get_conf('JWT', 'SEC_KEY')
cipher = AESCipher(secret_key)

if __name__ == '__main__':
    import secrets

    key_hex = secrets.token_hex(16)  # 生成十六进制字符串
    key_bytes = bytes.fromhex(key_hex)  # 转换为字节字符串
    print(key_hex)

    passwd = 'zaq1xsw2cde'
    encrypted = cipher.encrypt(passwd)  # 加密
    print(encrypted)

    decrypted = cipher.decrypt(encrypted)  # 解密
    print(decrypted)
