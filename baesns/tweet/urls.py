# tweet/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'), # 127.0.0.1:8000 과 views.py 폴더의 home 함수 연결
    path('tweet/', views.tweet, name='tweet'),
    path('tweet/delete/<int:id>', views.delete_tweet, name='delete_tweet'),
    path('tweet/<int:id>', views.detail_tweet, name='detail_tweet'),
    path('tweet/comment/<int:id>', views.write_comment, name='write_comment'),
    path('tweet/comment/delete/<int:id>', views.delete_comment, name='delete_comment'),
]