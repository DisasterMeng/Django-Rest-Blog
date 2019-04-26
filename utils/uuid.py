import time
import random
import string
import hashlib


def md5(data):
    return hashlib.md5(data).hexdigest()


def random_string(num_min=8, num_max=15):
    random_num = random.randint(num_min, num_max)
    return ''.join(random.sample(string.ascii_letters + string.digits, random_num))


def uuid(data):
    random_str = random_string()
    if data:
        random_str += data
    random_str += str(time.time())
    return md5(random_str.encode('utf-8'))
