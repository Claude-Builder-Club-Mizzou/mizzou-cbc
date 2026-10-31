from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('gallery/', views.gallery, name='gallery'),
    path('benefits/', views.benefits, name='benefits'),
    path('team/', views.team, name='team'),
    path('projects/', views.projects, name='projects'),
    path('projects/<slug:slug>/', views.project_detail, name='project_detail'),
    path('builders/<slug:slug>/', views.builder_detail, name='builder_detail'),
    path('connect/', views.connect, name='connect'),
]
