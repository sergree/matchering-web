import random
import string
import os


def random_str_func(k):
    def random_str():
        return ''.join(random.choices(string.ascii_letters + string.digits, k=k))
    return random_str


def random_str_32():
    return random_str_func(32)()


def without_folder(path):
    return os.path.splitext(os.path.basename(path))[0]


def get_directory(path):
    return os.path.dirname(path)


def join(path1, path2):
    return os.path.join(path1, path2)


def generate_filename(ext='wav', bit=16, title=None):
    if title:
        return f'Matchering_{bit}bit_{title}_{random_str_func(4)()}.{ext}'
    else:
        return f'{random_str_func(16)()}.{ext}'
