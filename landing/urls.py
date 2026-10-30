from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('gallery/', views.gallery, name='gallery'),
    path('benefits/', views.benefits, name='benefits'),
    path('team/', views.team, name='team'),
    path('projects/', views.projects, name='projects'),
    path('connect/', views.connect, name='connect'),
]
