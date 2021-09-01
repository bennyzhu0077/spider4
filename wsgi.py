# coding: utf-8
import os
import leancloud
from gevent.pywsgi import WSGIServer
from django.core.wsgi import get_wsgi_application

APP_ID = os.environ['LC_APP_ID']
MASTER_KEY = os.environ['LC_APP_MASTER_KEY']
PORT = int(os.environ['LC_APP_PORT'])

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "spider_project.settings")

leancloud.init(APP_ID, master_key=MASTER_KEY)
app = get_wsgi_application()
engine = leancloud.Engine(app)
application = engine

if __name__ == '__main__':
    # 只在本地开发环境执行的代码
    server = WSGIServer(('localhost', PORT), application)
    server.serve_forever()
