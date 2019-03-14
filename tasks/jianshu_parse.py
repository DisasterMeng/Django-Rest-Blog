import re

import requests
from bs4 import BeautifulSoup

from tasks.tomd import Tomd


# print(res.text)




def parse_jianshu(text):
    soup = BeautifulSoup(text, 'html.parser')

    content = soup.select_one('div.show-content-free')
    m = re.search('div\sclass="show-content-free">([\s\S]*)</div>', str(content))
    if m:
        html = m.group(1)
        content= Tomd(html=html).markdown

    title = soup.title.string.string.replace(' - 简书','')

    date = soup.find('span',class_='publish-time').string.replace('*','')
    views = 0
    all = re.findall(r'"views_count":(\d+?),',text)
    if len(all)>0:
        views = all[0]

    category = soup.select_one('.notebook span').string

    return {
        'content':content,
        'title':title,
        'date':date,
        'views':views,
        'category':category

    }


if __name__ == '__main__':
    headers = {
        'referer': 'https://www.jianshu.com/u/debdd7d8eb03',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36'
    }

    url = 'https://www.jianshu.com/p/e822329a0137'

    res = requests.get(url=url, headers=headers)



    option = parse_jianshu(res.text)
    print(option)


