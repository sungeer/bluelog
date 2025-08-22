import configparser
import time
from pathlib import Path
from binascii import a2b_hex

import httpx
from Crypto.Cipher import AES  # pip install pycryptodome


class ConfigDetector:

    def __init__(self, conf_dir=None, nacos_addr=None, namespace='prd', nacos_user=None, nacos_passwd=None):
        self.conf_dir = conf_dir
        self.nacos_addr = nacos_addr
        self.namespace = namespace
        self.nacos_user = nacos_user
        self.nacos_passwd = nacos_passwd
        self.load_conf()

    def load_conf(self):
        max_times = 10
        for i in range(max_times):
            try:
                self._load_conf()
            except (Exception,):
                time.sleep(1)
                continue
            else:
                break

    def _load_conf(self):
        self.config = configparser.ConfigParser()
        self.key = configparser.ConfigParser()
        if self.conf_dir:
            self.config.read(Path(self.conf_dir) / 'default_conf.ini')
            self.key.read(Path(self.conf_dir) / 'seckey_conf.ini')
        else:
            conf = self._get_client('viper_default_conf.ini', 'DEFAULT_GROUP')
            salt = self._get_client('viper_seckey_conf.ini', 'DEFAULT_GROUP')
            self.config.read_string(conf)
            self.key.read_string(salt)

    def _get_client(self, data_id, group):
        url = f'{self.nacos_addr}/nacos/v2/cs/config'
        params = {
            'dataId': data_id,
            'group': group,
        }
        response = httpx.get(url, params=params, timeout=30.0)
        return response.text

    def get_conf(self, section='DEFAULT', key='DEFAULT'):
        value = self.config.get(section, key)
        return value

    def get_sec_conf(self, section='DEFAULT', key='DEFAULT'):
        text = self.get_conf(section, key)
        seckey = self.key.get(section, key)
        if len(seckey) not in [32, 16]:
            raise ValueError(f'The length of the seckey must be 16 or 32, it cannot be {len(seckey)}.')
        aes = AES.new(seckey.encode(), AES.MODE_ECB)
        sec_conf = str(aes.decrypt(a2b_hex(text)), encoding='utf-8', errors='ignore')
        return sec_conf.strip()

    def get_boolean_conf(self, section='DEFAULT', key='DEFAULT'):
        value = self.config.getboolean(section, key)
        return value

    def get_int_conf(self, section='DEFAULT', key='DEFAULT'):
        value = self.config.getint(section, key)
        return value

    def get_float_conf(self, section='DEFAULT', key='DEFAULT'):
        value = self.config.getfloat(section, key)
        return value
