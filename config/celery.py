import os
from celery import Celery

# 設定 Django 的環境變數
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

# 建立 Celery 實例
app = Celery('nexus_mart')

# 讓 Celery 去 settings.py 讀取以 CELERY_ 開頭的設定
app.config_from_object('django.conf:settings', namespace='CELERY')

# 讓 Celery 自動去各個 app 裡找 tasks.py 來執行
app.autodiscover_tasks()