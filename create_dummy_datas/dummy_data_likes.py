import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')
import django
django.setup()

import random
import datetime
from music_memo.models import User, Song, Post, Like, Record
from collections import defaultdict
from faker import Faker
fake = Faker()

def add_likes():
    sets = defaultdict(list)
    other_sets = defaultdict(list)
    for i in range(50):
        random_user = User.objects.get(pk=random.randint(1,11))
        random_post=Post.objects.get(pk=random.randint(1,49))
        if random_post.pk not in sets[random_user.username] and random_post.user != random_user:
            sets[random_user.username].append(random_post.pk)
            like = Like.objects.get_or_create(post=random_post, user=random_user)[0]
            like.save()
        else:
            other_sets[random_user.username].append(random_post.pk)
    print("--")
    for k, v in other_sets.items():
        print(k, v)
    print("--")

if __name__ == "__main__":
    print('adding_likes')
    add_likes()
    print('all_added')