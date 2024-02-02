import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')
import django
django.setup()

import random
import datetime
from music_memo.models import User, Song, Post, Like, Record
from faker import Faker
fake = Faker()

def add_records():
    for i in range(50):
        memo_text = fake.text()
        random_song = Song.objects.get(pk=random.randint(1, 100))
        random_user = User.objects.get(pk=random.randint(1,11))
        now = datetime.datetime.now()
        a = fake.date_time()
        b = fake.date_time()
        random_date_start = min(a, b)
        random_date_end = max(a, b)
        record = Record.objects.get_or_create(memo=memo_text, date_start=random_date_start, date_end=random_date_end, song=random_song, user=random_user)[0]
        record.save()

if __name__ == "__main__":
    print('adding_records')
    add_records()
    print('all_added')