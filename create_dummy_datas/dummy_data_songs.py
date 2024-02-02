import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')
import django
django.setup()

import random
import string
import datetime
from music_memo.models import User, Song, Post, Like, Record
from faker import Faker
fake = Faker()

def add_songs():
    
    for x in range(100):
        song_name = fake.company()
        singer_name = fake.name()
        random_date = fake.date_time()
        random_user = User.objects.get(pk=random.randint(1,11))
        song = Song.objects.get_or_create(title=song_name, singer=singer_name, song_published_at=random_date, user=random_user)[0]
        song.save()

if __name__ == "__main__":
    print('adding_songs')
    add_songs()
    print('all_added')