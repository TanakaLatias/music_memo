import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')
import django
django.setup()

import random
import datetime
import string
from music_memo.models import User, Song, Post, Like, Record
from collections import defaultdict
from faker import Faker
fake = Faker()

def add_posts():
    sets = defaultdict(list)
    other_sets = defaultdict(list)
    for i in range(50):
        n = fake.text().split(".")
        post_name = fake.text().replace("\n", " ").replace(".", "")[:49]
        post_text = fake.text()
        random_song = Song.objects.get(pk=random.randint(1, 100))
        random_user = User.objects.get(pk=random.randint(1,11))
        if random_song.title not in sets[random_user.username]:
            sets[random_user.username].append(random_song.title)
            post = Post.objects.get_or_create(title=post_name, text=post_text, song=random_song, user=random_user)[0]
            post.save()
        else:
            other_sets[random_user.username].append(random_song.title)
    print("--")
    for k, v in other_sets.items():
        print(k, v)
    print("--")

if __name__ == "__main__":
    print('adding_posts')
    add_posts()
    print('all_added')