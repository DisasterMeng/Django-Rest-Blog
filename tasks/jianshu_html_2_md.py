import re

import requests
from bs4 import BeautifulSoup

from .tomd import Tomd


# print(res.text)


def html_2_md(res):
    soup = BeautifulSoup(res, 'html.parser')

    content = soup.select_one('div.show-content-free')
    # print(content)

    m = re.search('div\sclass="show-content-free">([\s\S]*)</div>', str(content))
    if m:
        html = m.group(1)
        return Tomd(html=html).markdown


if __name__ == '__main__':
    headers = {
        'referer': 'https://www.jianshu.com/u/debdd7d8eb03',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36'
    }

    url = 'https://www.jianshu.com/p/e822329a0137'

    res = requests.get(url=url, headers=headers)
    md=html_2_md(res.text)
    print(md)
