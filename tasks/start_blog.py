import datetime
import os
import random
import re
import time

import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings.dev')
django.setup()
import requests
from bs4 import BeautifulSoup
from django.conf import settings

from blog.models import Blog, Category
from tasks.jianshu_parse import parse_jianshu


def start_blog():
    session = requests.session()
    headers = {
        'referer': 'https://www.jianshu.com',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36'
    }
    session.headers = headers

    for page in range(1, 100):
        time.sleep(random.randint(5, 10))
        res = session.get(url=settings.JS_HOME + '?order_by=shared_at&page={}'.format(page))
        if res.status_code == 200:
            soup = BeautifulSoup(res.text, 'html.parser')
            lis = soup.find_all('li', id=re.compile("note"))
            for li in lis:
                href = li.select_one('a.title')['href']
                url = 'https://www.jianshu.com' + href
                time.sleep(random.randint(5, 10))
                res = session.get(url=url)
                if res.status_code == 200:
                    jianshu = parse_jianshu(res.text)
                    print(jianshu)
                    category_str = jianshu.get('category')
                    category = Category.objects.filter(name=category_str).first()
                    if category is None:
                        print('类别不存在 进行创建')
                        category = Category.objects.create(name=category_str)

                    title = jianshu.get('title')
                    blog = Blog.objects.filter(title=title).first()
                    if blog is None:
                        print('文章不存在 进行创建')
                        blog = Blog(title=title, category=category, content=jianshu.get('content'),
                                    page_view=jianshu.get('views'),
                                    created=datetime.datetime.strptime(jianshu.get('date'), '%Y.%m.%d %H:%M'))
                        blog.save()
        else:
            break


if __name__ == '__main__':
    start_blog()
