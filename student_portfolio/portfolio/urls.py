from django.urls import path
from .views import add_project
from . import views

urlpatterns = [
    path('add-project/', add_project, name='add_project'),
    path('projects/', views.project_list, name='projects'),
]