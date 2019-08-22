from .common import *

DEBUG = False
ALLOWED_HOSTS = ['.yandingblog.cn','localhost','127.0.0.1','0.0.0.0']


# 跨域设置
CORS_ORIGIN_ALLOW_ALL = False
CORS_ORIGIN_WHITELIST = (
    'localhost:10086',
    '127.0.0.1:10086',
    'sujian.yandingblog.cn',
    'img.cdn.yandingblog.cn'
)

#七牛
QINIU_ACCESS_KEY = ''
QINIU_SECRET_KEY = ''
QINIU_BUCKET_NAME = ''
QINIU_BUCKET_DOMAIN = ''
QINIU_SECURE_URL = False

PREFIX_URL = 'http://'
# 文件系统更改
MEDIA_URL = PREFIX_URL + QINIU_BUCKET_DOMAIN + "/media/"
MEDIA_ROOT = "media"
DEFAULT_FILE_STORAGE = 'qiniu_storage.backends.QiniuMediaStorage'


STATIC_URL = QINIU_BUCKET_DOMAIN + '/static/'
STATIC_ROOT = "static"
STATICFILES_STORAGE = 'qiniu_storage.backends.QiniuStaticStorage'


# github auth
GITHUB_APP_ID = ''
GITHUB_KEY = ''
GITHUB_CALLBACK_URL = ''

