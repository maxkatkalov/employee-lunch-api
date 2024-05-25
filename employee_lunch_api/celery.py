from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "employee_lunch_api.settings")

app = Celery("employee_lunch_api_task_queuer")

app.config_from_object("django.conf:settings", namespace="CELERY")

app.autodiscover_tasks()
