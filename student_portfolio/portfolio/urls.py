from django.urls import path
from . import views

urlpatterns = [
    # Dashboard
    path('dashboard/', views.dashboard, name='dashboard'),
    path('theme/change/', views.change_theme, name='change_theme'),

    # Projects
    path('project/add/', views.project_create, name='project_create'),
    path('project/<int:pk>/', views.project_detail, name='project_detail'),
    path('project/<int:pk>/edit/', views.project_edit, name='project_edit'),
    path('project/<int:pk>/delete/', views.project_delete, name='project_delete'),

    # Skills
    path('skill/add/', views.skill_create, name='skill_create'),
    path('skill/<int:pk>/edit/', views.skill_edit, name='skill_edit'),
    path('skill/<int:pk>/delete/', views.skill_delete, name='skill_delete'),

    # Education
    path('education/add/', views.education_create, name='education_create'),
    path('education/<int:pk>/edit/', views.education_edit, name='education_edit'),
    path('education/<int:pk>/delete/', views.education_delete, name='education_delete'),

    # Experience
    path('experience/add/', views.experience_create, name='experience_create'),
    path('experience/<int:pk>/edit/', views.experience_edit, name='experience_edit'),
    path('experience/<int:pk>/delete/', views.experience_delete, name='experience_delete'),

    # Resume Template System
    path('resume/', views.resume_selection, name='resume_selection'),
    path('resume/preview/<str:template_name>/', views.resume_preview, name='resume_preview'),
    path('resume/preview-ajax/<str:template_name>/', views.resume_preview_ajax, name='resume_preview_ajax'),
    path('resume/download/<str:template_name>/', views.resume_download, name='resume_download'),

    # Public portfolio — MUST be last (catches any slug)
    path('portfolio/<slug:slug>/', views.public_portfolio, name='public_portfolio'),
]