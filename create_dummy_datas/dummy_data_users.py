import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')
import django
django.setup()

import random
import datetime
from music_memo.models import User, Song, Post, Like, Record

users=["sawasawa", "chomi", "pola", "fin", "kyl", "sam", "gab", "wil", "ben", "jet"]
passes=["watashinonamae", "kitakami", "hachiware", "foxhound", "kelpiedog", "sennenhund", "goldenretriever", "waterspaniel", "bolognese", "labradorretriever"]

def add_users():
    l=int(len(users))
    for i in range(l):
        user = User.objects.get_or_create(username=users[i], password=passes[i], email=users[i]+"@carter.com")[0]
        user.save()

if __name__ == "__main__":
    print('adding_users')
    add_users()
    print('all_added')