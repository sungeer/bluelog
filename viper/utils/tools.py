import secrets
from datetime import datetime


def generate_random_id(byte_length: int = 16) -> str:
    return secrets.token_hex(byte_length)


def current_time():
    return datetime.now()
