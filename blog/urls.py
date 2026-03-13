from django.urls import path
from . import views

urlpatterns = [
    path('', views.blog_list, name='blog_list'),
    path('new/', views.blog_create, name='blog_create'),
    path('<slug:slug>/', views.blog_detail, name='blog_detail'),
    path('<slug:slug>/edit/', views.blog_edit, name='blog_edit'),
    path('<slug:slug>/delete/', views.blog_delete, name='blog_delete'),
    path('<slug:slug>/like/', views.like_post, name='like_post'),
    path('comment/<int:pk>/edit/', views.edit_comment, name='edit_comment'),
    path('comment/<int:pk>/delete/', views.delete_comment, name='delete_comment'),
]
