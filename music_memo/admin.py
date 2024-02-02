from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import ugettext_lazy as _
from .models import User, Song, Post, Like, Record
from django.contrib.auth.models import Group

class MyUserAdmin(UserAdmin):
    fieldsets = (
        (None, {'fields': ('username', 'email', 'description', 'password', 'is_staff', 'is_active', 'is_superuser', 'last_login', 'date_joined', 'hide_your_posts', 'hide_favorite_posts', 'hide_your_records')}),
    )
    add_fieldsets = (
        (None, {'fields': ('email', 'username', 'password1', 'password2'),}),
    )
    list_display = ('pk', 'email', 'username')
    ordering = ('-pk',)

class SongAdmin(admin.ModelAdmin):
    list_display = ('pk', 'singer', 'title', 'song_published_at', 'user')
    search_fields = ('singer', 'title', 'song_published_at', 'user__email__icontains')
    ordering = ('-pk',)

class PostAdmin(admin.ModelAdmin):
    list_display = ('pk', 'song', 'user', 'hide')
    search_fields = ('song__title__icontains', 'user__email__icontains')
    ordering = ('-pk',)

class LikeAdmin(admin.ModelAdmin):
    list_display = ('pk', 'user', 'post')
    search_fields = ('post__user__username__icontains', 'user__email__icontains')
    ordering = ('-pk',)

class RecordAdmin(admin.ModelAdmin):
    list_display = ('pk', 'user', 'song', 'hide')
    search_fields = ('song__title__icontains', 'user__email__icontains')
    ordering = ('-pk',)

admin.site.register(User, MyUserAdmin)
admin.site.register(Song, SongAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(Like, LikeAdmin)
admin.site.register(Record, RecordAdmin)
admin.site.unregister(Group)