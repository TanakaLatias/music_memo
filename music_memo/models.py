from tkinter import CASCADE
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.db.models import UniqueConstraint
from django.contrib.auth.validators import ASCIIUsernameValidator
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError

class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, username, password, **extra_fields):
        if not email:
            raise ValueError('Users must have an email.')
        if not username:
            raise ValueError('Users must have a username.')
        email = self.normalize_email(email)
        username = self.model.normalize_username(username)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self.db)
        return user
    
    def create_user(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, username, password, **extra_fields)

    def create_superuser(self, username, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        if extra_fields.get('is_staff') is not True:
            raise ValueError('is_staff must be true.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('is_superuser must be true.')
        return self._create_user(email, username, password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    username_validator = ASCIIUsernameValidator()

    username = models.CharField(_("username"), max_length=50, validators=[username_validator])
    email = models.EmailField(_("email"), unique=True)
    description = models.TextField(_("description"), blank=True, null=True)
    is_staff = models.BooleanField(_("is_staff"), default=False)
    is_active = models.BooleanField(_("is_active"), default=True)
    date_joined = models.DateTimeField(_("date joined"), default=timezone.now)
    hide_your_posts = models.BooleanField(_("hide_your_posts"), default=False)
    hide_favorite_posts = models.BooleanField(_("hide_favorite_posts"), default=False)
    hide_your_records = models.BooleanField(_("hide_your_records"), default=False)

    objects = UserManager()
    USERNAME_FIELD = "email"
    EMAIL_FIELD = "email"
    REQUIRED_FIELDS = ['username']

    class Meta:
        ordering = ['date_joined']
    def __str__(self):
        return self.email
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.hide_your_posts:
            Post.objects.filter(user=self, hide=False).update(hide=True)
        else:
            Post.objects.filter(user=self, hide=True).update(hide=False)
        if self.hide_favorite_posts:
            Like.objects.filter(user=self, hide=False).update(hide=True)
        else:
            Like.objects.filter(user=self, hide=True).update(hide=False)
        if self.hide_your_records:
            Record.objects.filter(user=self, hide=False).update(hide=True)
        else:
            Record.objects.filter(user=self, hide=True).update(hide=False)

class Song(models.Model):
    title = models.CharField(max_length=50)
    singer = models.CharField(max_length=50)
    song_published_at = models.DateField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    def visible_post_count(self):
        return self.post_set.filter(hide=False).count()
    def visible_record_count(self):
        return self.record_set.filter(hide=False).count()
    def __str__(self):
        return f'{self.singer} : {self.title}'
    class Meta:
        ordering = ('singer', 'title',)
        unique_together = ['title', 'singer']

class Post(models.Model):
    title = models.CharField(max_length=50)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)
    image = models.ImageField(null=True, blank=True, upload_to="images/")
    song = models.ForeignKey(Song, on_delete=models.CASCADE)
    hide = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    def __str__(self):
        return f'{self.song} : {self.user.username}'
    class Meta:
        ordering = ('song',)
    class Meta:
        constraints = [UniqueConstraint(fields=['user', 'song'], name='unique_post')]

class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    hide = models.BooleanField(default=False)
    def __str__(self):
        return f'{self.user} : {self.post.user.username}'
    class Meta:
        constraints = [UniqueConstraint(fields=['user', 'post'], name='unique_like')]

class Record(models.Model):
    memo = models.TextField()
    date_start = models.DateField(null=True, blank=True, default=timezone.now)
    date_end = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    song = models.ForeignKey(Song, on_delete=models.CASCADE)
    hide = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    def __str__(self):
        return f'{self.user} : {self.song.title}'
    def clean(self):
        if self.date_start and self.date_end and self.date_start > self.date_end:
            raise ValidationError('It seems that your date_start and date_end are the other way around.')
    def days(self):
        if self.date_start and self.date_end:
            delta = self.date_end - self.date_start
            return delta.days
        else:
            return None