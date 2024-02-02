from django.urls import path
from .views import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    #top
    path('', TopAndIndexView.as_view(), name='top'),
    #users
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('my_page/', MyPageView.as_view(), name='my_page'),
    path('my_posts/', MyPostsView.as_view(), name='my_posts'),
    path('my_likes/', MyLikesView.as_view(), name='my_likes'),
    path('my_records/', MyRecordsView.as_view(), name='my_records'),
    path('user_detail/<int:pk>/', UserDetailView.as_view(), name='user_detail'),
    path('user_detail_posts/<int:pk>/', UserDetailPostsView.as_view(), name='user_detail_posts'),
    path('user_detail_likes/<int:pk>/', UserDetailLikesView.as_view(), name='user_detail_likes'),
    path('user_detail_records/<int:pk>/', UserDetailRecordsView.as_view(), name='user_detail_records'),
    path('user_create/', UserCreateView.as_view(), name='user_create'),
    path('user_update/', UserUpdateView.as_view(), name='user_update'),
    #songs
    path('song_index/', SongIndexView.as_view(), name='song_index'),
    path('song_index_posted/', SongIndexPostedView.as_view(), name='song_index_posted'),
    path('song_index_recorded/', SongIndexRecordedView.as_view(), name='song_index_recorded'),
    path('song_search/', SongSearchView.as_view(), name='song_search'),
    path('song_detail_post/<int:pk>/', SongDetailPostView.as_view(), name='song_detail_post'),
    path('song_detail_record/<int:pk>/', SongDetailRecordView.as_view(), name='song_detail_record'),
    path('song_create/', SongCreateView.as_view(), name='song_create'),
    path('song_update/<int:pk>/', SongUpdateView.as_view(), name='song_update'),
    #path('song_delete/<int:pk>/', SongDeleteView.as_view(), name='song_delete'),
    #posts
    path('post_index/', PostIndexView.as_view(), name='post_index'),
    path('post_search/', PostSearchView.as_view(), name='post_search'),
    path('post_detail/<int:pk>/', PostDetailView.as_view(), name='post_detail'),
    path('post_create/', PostCreateView.as_view(), name='post_create'),
    path('song_detail_post_create/<int:pk>/', SongDetailPostCreateView.as_view(), name='song_detail_post_create'),
    path('post_update/<int:pk>/', PostUpdateView.as_view(), name='post_update'),
    path('post_delete/<int:pk>/', PostDeleteView.as_view(), name='post_delete'),
    #likes
    path('like_create/<int:pk>/', LikeCreateView.as_view(), name='like_create'),
    path('like_delete/<int:pk>/', LikeDeleteView.as_view(), name='like_delete'),
    #records
    path('record_index/', RecordIndexView.as_view(), name='record_index'),
    path('record_search/', RecordSearchView.as_view(), name='record_search'),
    path('record_detail/<int:pk>/', RecordDetailView.as_view(), name='record_detail'),
    path('record_create/', RecordCreateView.as_view(), name='record_create'),
    path('song_detail_record_create/<int:pk>/', SongDetailRecordCreateView.as_view(), name='song_detail_record_create'),
    path('record_update/<int:pk>/', RecordUpdateView.as_view(), name='record_update'),
    path('record_delete/<int:pk>/', RecordDeleteView.as_view(), name='record_delete'),
    #errors
    path('error/',ErrorView.as_view(), name='error'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
