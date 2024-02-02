from .models import Post, Song, Record, User
from django.db.models import Count, Q
from django.utils import timezone
from django.db.models import Max, F
from django.db.models.functions import Coalesce

def side_new_songs(request):
    side_new_songs = Song.objects.order_by('-pk')[:10]
    return {'side_new_songs': side_new_songs}

def side_new_posts(request):
    side_new_posts = Post.objects.filter(hide=False).order_by('-pk')[:10]
    return {'side_new_posts': side_new_posts}

def side_new_records(request):
    side_new_records = Record.objects.filter(hide=False, date_start__isnull=False, date_end__isnull=False).order_by('-pk')[:10]
    return {'side_new_records': side_new_records}