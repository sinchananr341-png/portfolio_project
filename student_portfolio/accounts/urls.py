from django.urls import path
from .views import register, dashboard

urlpatterns = [
    path('register/', register, name='register'),
    path('dashboard/', dashboard, name='dashboard'),
    path('create-profile/', create_profile, name='create_profile'),
]