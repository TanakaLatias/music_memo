from django.shortcuts import reverse, redirect, get_object_or_404
from time import timezone
import datetime
from django.utils import timezone
from django.urls import reverse_lazy
from django.contrib.auth import login
from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.views import LoginView, LogoutView
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import MyUserCreationForm, MyUserChangeForm, LoginForm, SongForm, PostForm, RecordForm
from .models import User, Song, Post, Like, Record
from django.db.models import Count, Q
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db import IntegrityError

class UserCheckMixin:
    def get(self, request, *args, **kwargs):
        object = self.get_object()
        if object.user != self.request.user:
            return redirect('error')
        return super().get(request, *args, **kwargs)

class MyCreateView(LoginRequiredMixin, CreateView):
    template_name = 'htmls/basic_form.html'
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class TopAndIndexView(TemplateView):
    template_name = 'htmls/top.html'

class LoginView(LoginView):
    form_class = LoginForm
    template_name = 'htmls/basic_form.html'

class MyPageView(LoginRequiredMixin, TemplateView):
    template_name = 'htmls/my_page.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['my_page'] = 'my_page'
        me = self.request.user
        context['user'] = me
        context['posts'] = Post.objects.filter(user=me).order_by('-created_at')[:5]
        context['likes'] = Like.objects.filter(user=me).order_by('-created_at')[:5]
        context['records'] = Record.objects.filter(user=me).order_by('-date_start')[:5]
        context['posts_count'] = Post.objects.filter(user=me).count()
        context['likes_count'] = Like.objects.filter(user=me).count()
        context['records_count'] = Record.objects.filter(user=me).count()
        context['visible_posts_count'] = Post.objects.filter(user=me, hide=False).count()
        context['visible_likes_count'] = Like.objects.filter(user=me, hide=False).count()
        context['visible_records_count'] = Record.objects.filter(user=me, hide=False).count()
        return context

class MyPostsView(LoginRequiredMixin, ListView):
    model = Post
    context_object_name = 'posts'
    template_name = 'htmls/my_page.html'
    paginate_by = 10
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['my_posts'] = 'my_posts'
        me = self.request.user
        context['recent'] =  timezone.now() - datetime.timedelta(days=3)
        context['posts_count'] = Post.objects.filter(user=me).count()
        context['visible_posts_count'] = Post.objects.filter(user=me, hide=False).count()
        return context
    def get_queryset(self):
        me = self.request.user
        return Post.objects.filter(user=me).order_by('-created_at')

class MyLikesView(LoginRequiredMixin, ListView):
    model = Like
    context_object_name = 'likes'
    template_name = 'htmls/my_page.html'
    paginate_by = 10
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['my_likes'] = 'my_likes'
        me = self.request.user
        context['recent'] =  timezone.now() - datetime.timedelta(days=3)
        context['likes_count'] = Like.objects.filter(user=me).count()
        context['visible_likes_count'] = Like.objects.filter(user=me, hide=False).count()
        return context
    def get_queryset(self):
        me = self.request.user
        return Like.objects.filter(user=me).order_by('-created_at')

class MyRecordsView(LoginRequiredMixin, ListView):
    model = Record
    context_object_name = 'records'
    template_name = 'htmls/my_page.html'
    paginate_by = 30
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['my_records'] = 'my_records'
        me = self.request.user
        context['records_count'] = Record.objects.filter(user=me).count()
        context['visible_records_count'] = Record.objects.filter(user=me, hide=False).count()
        return context
    def get_queryset(self):
        me = self.request.user
        return Record.objects.filter(user=me).order_by('-date_start', '-pk')

class UserDetailView(DetailView):
    model = User
    template_name = 'htmls/user_detail.html'
    context_object_name = 'user'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_detail'] = 'user_detail'
        the_user = User.objects.get(id=self.kwargs.get('pk'))
        context['posts'] = Post.objects.filter(user=the_user, hide=False).order_by('-created_at')[:5]
        context['likes'] = Like.objects.filter(user=the_user, hide=False).order_by('-created_at')[:5]
        context['records'] = Record.objects.filter(user=the_user, hide=False).order_by('-date_start')[:5]
        context['visible_posts_count'] = Post.objects.filter(user=the_user, hide=False).count()
        context['visible_likes_count'] = Like.objects.filter(user=the_user, hide=False).count()
        context['visible_records_count'] = Record.objects.filter(user=the_user, hide=False).count()
        return context

class UserDetailPostsView(ListView):
    model = Post
    context_object_name = 'posts'
    template_name = 'htmls/user_detail.html'
    paginate_by = 10
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_detail_posts'] = 'user_detail_posts'
        the_user = User.objects.get(id=self.kwargs.get('pk'))
        context['user'] = the_user
        context['recent'] =  timezone.now() - datetime.timedelta(days=3)
        context['visible_posts_count'] = Post.objects.filter(user=the_user, hide=False).count()
        return context
    def get_queryset(self):
        the_user = User.objects.get(id=self.kwargs.get('pk'))
        return Post.objects.filter(user=the_user, hide=False).order_by('-created_at')

class UserDetailLikesView(ListView):
    model = Like
    context_object_name = 'likes'
    template_name = 'htmls/user_detail.html'
    paginate_by = 10
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_detail_likes'] = 'user_detail_likes'
        the_user = User.objects.get(id=self.kwargs.get('pk'))
        context['user'] = the_user
        context['visible_likes_count'] = Like.objects.filter(user=the_user, hide=False).count()
        return context
    def get_queryset(self):
        the_user = User.objects.get(id=self.kwargs.get('pk'))
        return Like.objects.filter(user=the_user, hide=False).order_by('-created_at')

class UserDetailRecordsView(ListView):
    model = Record
    context_object_name = 'records'
    template_name = 'htmls/user_detail.html'
    paginate_by = 30
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_detail_records'] = 'user_detail_records'
        the_user = User.objects.get(id=self.kwargs.get('pk'))
        context['user'] = the_user
        context['visible_records_count'] = Record.objects.filter(user=the_user, hide=False).count()
        return context
    def get_queryset(self):
        the_user = User.objects.get(id=self.kwargs.get('pk'))
        return Record.objects.filter(user=the_user, hide=False).order_by('-date_start')

class UserCreateView(CreateView):
    model = User
    form_class = MyUserCreationForm
    template_name = 'htmls/basic_form.html'
    success_url = reverse_lazy('top')
    def form_valid(self, form):
        try:
            response = super().form_valid(form)
            user = form.save()
            login(self.request, user)
            return redirect(reverse('my_page'))
        except IntegrityError:
            return redirect(reverse('error'))

class UserUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = MyUserChangeForm
    template_name = 'htmls/basic_form.html'
    def get_object(self, queryset=None):
        return self.request.user
    def get_success_url(self):
        return reverse('my_page')
    
class SongIndexView(ListView):
    model = Song
    context_object_name = 'songs'
    template_name = 'htmls/song_index.html'
    paginate_by = 50
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['index'] = 'index'
        return context
    def get_queryset(self):
        return Song.objects.order_by('singer', 'title')
    
class SongIndexPostedView(ListView):
    model = Song
    context_object_name = 'songs'
    template_name = 'htmls/song_index.html'
    paginate_by = 50
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['index_posted'] = 'index_posted'
        return context
    def get_queryset(self):
        return Song.objects.annotate(post_count=Count('post', filter=Q(post__hide=False))).order_by('-post_count', 'singer', 'title')
    
class SongIndexRecordedView(ListView):
    model = Song
    context_object_name = 'songs'
    template_name = 'htmls/song_index.html'
    paginate_by = 50
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['index_recorded'] = 'index_recorded'
        return context
    def get_queryset(self):
        return Song.objects.annotate(record_count=Count('record', filter=Q(record__hide=False))).order_by('-record_count', 'singer', 'title')

class SongSearchView(ListView):
    model = Song
    context_object_name = 'search_results'
    template_name = 'htmls/song_index.html'
    def get_queryset(self):
        query = self.request.GET.get('q')
        if query:
            return Song.objects.filter(Q(title__icontains=query) | Q(singer__icontains=query)).order_by('singer', 'title')
        else:
            return Song.objects.none()
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['song_search'] = 'song_search'
        context['search_query'] = self.request.GET.get('q', '')
        return context

class SongDetailPostView(ListView):
    model = Post
    context_object_name = 'posts'
    template_name = 'htmls/song_detail.html'
    paginate_by = 30
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['song'] = Song.objects.get(pk=self.kwargs.get('pk'))
        context['song_detail_post'] = 'song_detail_post'
        if self.request.user.is_authenticated:
            query = Post.objects.filter(user=self.request.user, song__pk=self.kwargs.get('pk'))
            if query.exists():
                context['your_post'] = Post.objects.get(pk=query.first().pk)
        return context
    def get_queryset(self):
        return Post.objects.filter(song=Song.objects.get(pk=self.kwargs.get('pk')), hide=False).order_by('created_at')
    
class SongDetailRecordView(ListView):
    model = Record
    context_object_name = 'records'
    template_name = 'htmls/song_detail.html'
    paginate_by = 30
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['song'] = Song.objects.get(pk=self.kwargs.get('pk'))
        context['song_detail_record'] = 'song_detail_record'
        if self.request.user.is_authenticated:
            context['your_records'] = Record.objects.filter(user=self.request.user, song__pk=self.kwargs.get('pk'))
        return context
    def get_queryset(self):
        return Record.objects.filter(song=Song.objects.get(pk=self.kwargs.get('pk')), hide=False).order_by('-date_start')
    
class SongCreateView(MyCreateView):
    model = Song
    form_class = SongForm
    success_url = reverse_lazy('top')
    def form_valid(self, form):
        try:
            response = super().form_valid(form)
            return redirect(reverse('song_detail_post', kwargs={'pk': self.object.pk}))
        except IntegrityError:
            return redirect(reverse('error'))

class SongUpdateView(LoginRequiredMixin, UpdateView):
    model = Song
    form_class = SongForm
    template_name = 'htmls/basic_form.html'
    def get_success_url(self):
        return reverse('song_detail_post', kwargs={'pk': self.kwargs.get('pk')})

class SongDeleteView(LoginRequiredMixin, DeleteView):
    model = Song
    context_object_name = 'song'
    template_name = 'htmls/basic_delete.html'
    success_url = reverse_lazy('song_index')

class PostIndexView(ListView):
    model = Post
    context_object_name = 'posts'
    template_name = 'htmls/post_index.html'
    paginate_by = 10
    def get_queryset(self):
        return Post.objects.filter(hide=False).order_by('-pk')
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['recent'] =  timezone.now() - datetime.timedelta(days=3)
        return context

class PostSearchView(ListView):
    model = Post
    context_object_name = 'search_results'
    template_name = 'htmls/post_index.html'
    def get_queryset(self):
        query = self.request.GET.get('q')
        if query:
            return Post.objects.filter(Q(title__icontains=query) | Q(text__icontains=query)).order_by('-pk')
        else:
            return Post.objects.none()
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['post_search'] = 'post_search'
        context['search_query'] = self.request.GET.get('q', '')
        return context

class PostDetailView(DetailView):
    model = Post
    template_name = 'htmls/post_detail.html'
    context_object_name = 'post'
    def get(self, request, *args, **kwargs):
        post = self.get_object()
        if post.hide and post.user != self.request.user:
            return redirect('error')
        return super().get(request, *args, **kwargs)
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            try:
                liked = Like.objects.get(user=self.request.user, post=Post.objects.get(pk=self.kwargs['pk']))
                context['liked'] = liked
            except Like.DoesNotExist:
                context['liked'] = None
        else:
            context['liked'] = None
        context['liked_count'] = Like.objects.filter(post=Post.objects.get(pk=self.kwargs['pk'])).count()
        return context
    
class PostCreateView(MyCreateView):
    model = Post
    form_class = PostForm
    success_url = reverse_lazy('top')
    def form_valid(self, form):
        try:
            response = super().form_valid(form)
            return redirect(reverse('post_detail', kwargs={'pk': self.object.pk}))
        except IntegrityError:
            return redirect(reverse('error'))
        
class SongDetailPostCreateView(MyCreateView):
    model = Post
    form_class = PostForm
    success_url = reverse_lazy('top')
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        default_song = Song.objects.get(pk=self.kwargs.get('pk'))
        kwargs['default_song'] = default_song
        return kwargs
    def form_valid(self, form):
        try:
            response = super().form_valid(form)
            return redirect(reverse('post_detail', kwargs={'pk': self.object.pk}))
        except IntegrityError:
            return redirect(reverse('error'))
        
class PostUpdateView(LoginRequiredMixin, UserCheckMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'htmls/basic_form.html'
    success_url = reverse_lazy('top')
    def form_valid(self, form):
        try:
            response = super().form_valid(form)
            return redirect(reverse('post_detail', kwargs={'pk': self.kwargs.get('pk')}))
        except IntegrityError:
            return redirect(reverse('error'))

class PostDeleteView(LoginRequiredMixin, UserCheckMixin, DeleteView):
    model = Post
    template_name = 'htmls/basic_delete.html'
    context_object_name = 'post'
    success_url = reverse_lazy('post_index')

class LikeCreateView(LoginRequiredMixin, CreateView):
    model = Like
    fields = []
    template_name = 'htmls/basic_form.html'
    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.post = Post.objects.get(pk=self.kwargs['pk'])
        try:
            if form.instance.post.hide:
                return redirect('error')
            form.save()
            return redirect('post_detail', pk=self.kwargs['pk'])
        except IntegrityError:
            return redirect('error')

class LikeDeleteView(LoginRequiredMixin, TemplateView):
    template_name = 'htmls/basic_delete.html'
    def get_object(self, queryset=None):
        return Like.objects.get(user=self.request.user, post=Post.objects.get(pk=self.kwargs['pk']))
    def post(self, request, *args, **kwargs):
        like = get_object_or_404(Like, user=self.request.user, post=Post.objects.get(pk=self.kwargs['pk']))
        like.delete()
        return redirect(reverse_lazy('post_detail', kwargs={'pk': self.kwargs['pk']}))

class RecordIndexView(ListView):
    model = Record
    context_object_name = 'records'
    template_name = 'htmls/record_index.html'
    paginate_by = 30
    def get_queryset(self):
        return Record.objects.filter(hide=False).order_by('-pk')

class RecordSearchView(ListView):
    model = Record
    context_object_name = 'search_results'
    template_name = 'htmls/record_index.html'
    def get_queryset(self):
        query = self.request.GET.get('q')
        if query:
            return Record.objects.filter(Q(memo__icontains=query) | Q(song__title__icontains=query)).order_by('-pk')
        else:
            return Record.objects.none()
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['record_search'] = 'record_search'
        context['search_query'] = self.request.GET.get('q', '')
        return context

class RecordDetailView(DetailView):
    model = Record
    context_object_name = 'record'
    template_name = 'htmls/record_detail.html'
    def get(self, request, *args, **kwargs):
        record = self.get_object()
        if record.hide and record.user != self.request.user:
            return redirect('error')
        return super().get(request, *args, **kwargs)

class RecordCreateView(MyCreateView):
    model = Record
    form_class = RecordForm
    success_url = reverse_lazy('top')
    def form_valid(self, form):
        response = super().form_valid(form)
        return redirect(reverse('record_detail', kwargs={'pk': self.object.pk}))
   
class SongDetailRecordCreateView(MyCreateView):
    model = Record
    form_class = RecordForm
    success_url = reverse_lazy('top')
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        default_song = Song.objects.get(pk=self.kwargs.get('pk'))
        kwargs['default_song'] = default_song
        return kwargs
    def form_valid(self, form):
        response = super().form_valid(form)
        return redirect(reverse('record_detail', kwargs={'pk': self.object.pk}))

class RecordUpdateView(LoginRequiredMixin, UserCheckMixin, UpdateView):
    model = Record
    form_class = RecordForm
    template_name = 'htmls/basic_form.html'
    def get_success_url(self):
        return reverse('record_detail', kwargs={'pk': self.kwargs.get('pk')})

class RecordDeleteView(LoginRequiredMixin, UserCheckMixin, DeleteView):
    model = Record
    template_name = 'htmls/basic_delete.html'
    context_object_name = 'record'
    success_url = reverse_lazy('record_index')

class ErrorView(TemplateView):
    template_name = 'htmls/error.html'