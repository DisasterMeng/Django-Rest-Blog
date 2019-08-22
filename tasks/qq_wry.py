import os
import django
from functools import wraps

from utils.uuid import md5
from utils.qqwry import QQwry
from utils.cz88update import updateQQwry

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings.dev')
django.setup()

from qq_wry.models import QqWry


try:
    from apscheduler.schedulers.background import BackgroundScheduler
    from django_apscheduler.jobstores import DjangoJobStore, register_events, register_job

    scheduler = BackgroundScheduler()
    scheduler.add_jobstore(DjangoJobStore(), "default")

    # 每天早上 9 点 更新qq_wry数据库
    @register_job(scheduler, 'cron', day_of_week='mon-fri', hour='9', minute='00', second='00')
    def run():
        wry = Wry()
        wry.task()

    register_events(scheduler)
    scheduler.start()
except Exception as e:
    # 有错误就停止定时器
    # scheduler.shutdown()
    pass


# 单例装饰器
def singleton(cls):
    instances = {}

    @wraps(cls)
    def get_instance(*args, **kwargs):
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]

    return get_instance


@singleton
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

    @staticmethod
    def update():
        res = updateQQwry()
        if type(res) == int:
            raise Exception('qqwry update fail')
        return res

    def task(self):
        # 比较md5 来决定是否更新
        try:
            print('开始更新qq_wry')
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
        except Exception as e:
            print(e)


if __name__ == '__main__':
    qq_wry = Wry()
    print(qq_wry.ip_search('127.0.0.1'))
    print(qq_wry.get_version())
    qq_wry.task()
