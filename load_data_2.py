"""Загружает data.sql через Django ORM. Запуск: python manage.py shell < load_data.py  или  python load_data.py"""
import os
import sys

import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
sys.path.insert(0, os.path.dirname(__file__))
django.setup()

from django.db import connection

with open(os.path.join(os.path.dirname(__file__), 'data.sql'), encoding='utf-8') as f:
    sql = f.read()

with connection.cursor() as cursor:
    cursor.execute("SELECT COUNT(*) FROM video_cards")
    if cursor.fetchone()[0] == 0:
        connection.connection.executescript(sql)
        print('Данные загружены.')
    else:
        print('Данные уже есть, пропускаю.')
