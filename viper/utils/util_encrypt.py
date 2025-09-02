import random
import string


def generate_password(length=12):
    if length < 12 or length > 64:
        raise ValueError('Password length must be between 12 and 64 characters.')

    # 定义字符集
    digits = string.digits
    lowers = string.ascii_lowercase
    uppers = string.ascii_uppercase
    specials = string.punctuation

    # 随机选择3种字符类型
    char_types = [digits, lowers, uppers, specials]
    selected_types = random.sample(char_types, 3)

    # 先保证每种都至少有一个
    password_chars = [random.choice(char_set) for char_set in selected_types]

    # 剩余的字符可从所有字符集中任选
    all_chars = ''.join(selected_types)
    password_chars += [random.choice(all_chars) for _ in range(length - 3)]

    # 打乱顺序
    random.shuffle(password_chars)
    return ''.join(password_chars)


if __name__ == '__main__':
    pwd = generate_password()
    print(pwd)
