# urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('pre-session/', views.pre_session_view, name='pre_session'),
    path('post-session/', views.post_session_view, name='post_session'),
    path('success_pre/', views.success_pre_view, name='success_pre'),
    path('success_post/', views.success_post_view, name='success_post'),
]
