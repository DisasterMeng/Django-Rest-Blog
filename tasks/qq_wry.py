import os
import time
import django
import schedule
import threading

from utils.uuid import md5
from utils.qqwry import QQwry
from utils.cz88update import updateQQwry

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings.dev')
django.setup()

from qq_wry.models import QqWry


class Wry:
    def __init__(self):
        self.wry = QqWry.objects.first()
        if not self.wry:
            self.wry = QqWry.objects.create()
            self.wry.file_save(self.update())
        self.wry_path = self.wry.qqwry_file.path
        self.q = QQwry()
        self.load_file()

    def load_file(self):
        self.q.load_file(self.wry_path)

    def ip_search(self, ip_address):
        result = self.q.lookup(ip_address)
        if type(result) == tuple:
            return ' '.join(result)
        else:
            return None

    def get_version(self):
        return self.q.get_lastone()

    def clear(self):
        self.q.clear()

    def update(self):
        res = updateQQwry()
        if type(res) == int:
            raise Exception('qqwry update fail')
        return res

    def task(self):
        # 比较md5 来决定是否更新
        try:
            cur_md5 = md5(self.wry.qqwry_file.read())
            wry_binary = self.update()
            up_md5 = md5(wry_binary)
            print('更新之前版本------ %s' % str(self.get_version()))
            if cur_md5 != up_md5:
                self.wry.file_save(wry_binary)
                self.wry.save()
                self.clear()
                self.load_file()
                print('更新之后版本----- %s' % str(self.get_version()))
            else:
                print('暂无更新')
        except Exception:
            print('qqwry task error')

    def run_threaded(self, func):
        threading.Thread(target=func).start()
        return schedule.CancelJob

    def run(self):
        schedule.every().day.at('09:00').do(self.run_threaded, self.task)
        while True:
            schedule.run_pending()
            time.sleep(1)


if __name__ == '__main__':
    qq_wry = Wry()
    print(qq_wry.ip_search('127.0.0.1'))
    print(qq_wry.get_version())
    qq_wry.task()
    # qq_wry.task()
