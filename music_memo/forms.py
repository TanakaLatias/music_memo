from dataclasses import fields
from django import forms
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, AuthenticationForm
from .models import User, Song, Post, Record

class MyForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['label'] = None
            field.widget.attrs['class'] = 'form'

class LoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['label'] = None
            field.widget.attrs['class'] = 'form'

class MyUserCreationForm(UserCreationForm, MyForm):
    class Meta:
        model = User
        fields = ['email', 'username', 'password1', 'password2']
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

class MyUserChangeForm(UserChangeForm, MyForm):
    class Meta:
        model = User
        fields = ['email', 'username', 'description', 'hide_your_posts', 'hide_favorite_posts', 'hide_your_records']
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password'].widget = forms.HiddenInput()
        self.fields['password'].help_text = None

class SongForm(forms.ModelForm):
    class Meta:
        model = Song
        fields = ['title', 'singer', 'song_published_at']
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['label'] = None
            field.widget.attrs['class'] = 'form'
        self.fields['song_published_at'].widget = forms.DateInput(attrs={'type': 'date'})

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'text', 'image', 'song', 'hide']
    def __init__(self, *args, **kwargs):
        default_song = kwargs.pop('default_song', None)
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['label'] = None
            field.widget.attrs['class'] = 'form'
        if default_song:
            self.fields['song'].initial = default_song

class RecordForm(forms.ModelForm):
    class Meta:
        model = Record
        fields = ['memo', 'date_start', 'date_end', 'song', 'hide']
    def __init__(self, *args, **kwargs):
        default_song = kwargs.pop('default_song', None)
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['label'] = None
            field.widget.attrs['class'] = 'form'
        self.fields['date_start'].widget = forms.DateInput(attrs={'type': 'date'})
        self.fields['date_end'].widget = forms.DateInput(attrs={'type': 'date'})
        if default_song:
            self.fields['song'].initial = default_song
