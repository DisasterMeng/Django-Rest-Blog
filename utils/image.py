import requests
from io import BytesIO


def img_download(url):
    '''
    返回流
    :param url:
    :return:
    '''

    return BytesIO(requests.get(url).content).getvalue()
