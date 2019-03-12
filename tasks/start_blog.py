import os

from django.conf import settings
import requests
import re
from bs4 import BeautifulSoup


def start_blog():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings.dev')
    session = requests.session()
    headers = {
        'referer': 'https://www.jianshu.com',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36'
    }
    session.headers = headers

    # res = session.get(url=settings.JS_HOME+'?order_by=shared_at&page=1')
    #     # print(res.text)

    s ="""<li id="note-25015101" data-note-id="25015101" class="">
  <div class="content">
    <a class="title" target="_blank" href="/p/99d1801a732a">react-navigation 嵌套 出现每个页面都能打开侧边</a>
    <p class="abstract">
      这个问题困扰了我一个多小时，尴尬。 问题是这个样子的，每个界面都能打开侧边: 路由代码: 百度搜索了下，没有搜索到解决方案，倒是搜到了和我一样的...
    </p>
    <div class="meta">
      <a target="_blank" href="/p/99d1801a732a">
        <i class="iconfont ic-list-read"></i> 684
</a>        <a target="_blank" href="/p/99d1801a732a#comments">
          <i class="iconfont ic-list-comments"></i> 4
</a>      <span><i class="iconfont ic-list-like"></i> 4</span>
      <span class="time" data-shared-at="2018-03-11T00:41:57+08:00"></span>
    </div>
  </div>
</li>


<li id="note-24692996" data-note-id="24692996" class="have-img">
    <a class="wrap-img" href="/p/e3e53c8e1c41" target="_blank">
      <img data-echo="//upload-images.jianshu.io/upload_images/2189945-27bc4d1dc6be598f.png?imageMogr2/auto-orient/strip|imageView2/1/w/300/h/240" class="img-blur" src="//upload-images.jianshu.io/upload_images/2189945-27bc4d1dc6be598f.png?imageMogr2/auto-orient/strip|imageView2/1/w/150/h/120" alt="120" />
    </a>
  <div class="content">
    <a class="title" target="_blank" href="/p/e3e53c8e1c41">React Native&amp;Redux state状态变化组件未更新</a>
    <p class="abstract">
      这个问题困扰我几天了，一直解决不了，各种尝试，才知道自己还差的很远。 首先，上面那个标题是错的 错的 错的，之所以这样写是方便搜索。 之所以没有...
    </p>
    <div class="meta">
      <a target="_blank" href="/p/e3e53c8e1c41">
        <i class="iconfont ic-list-read"></i> 211
</a>        <a target="_blank" href="/p/e3e53c8e1c41#comments">
          <i class="iconfont ic-list-comments"></i> 3
</a>      <span><i class="iconfont ic-list-like"></i> 4</span>
        <span><i class="iconfont ic-list-money"></i> 1</span>
      <span class="time" data-shared-at="2018-03-03T16:40:24+08:00"></span>
    </div>
  </div>
</li>"""

    soup = BeautifulSoup(s,'html.parser')
    lis = soup.find_all('li',id=re.compile("note"))
    urls = []
    for li in lis:
        href = li.select_one('a.title')['href']
        urls.append('https://www.jianshu.com'+href)








if __name__ == '__main__':
    start_blog()