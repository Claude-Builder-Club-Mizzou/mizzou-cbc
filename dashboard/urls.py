from django.urls import path

from . import views

app_name = 'dashboard'

urlpatterns = [
    path('', views.dashboard_login, name='login'),
    path('logout/', views.dashboard_logout, name='logout'),
    path('dashboard/', views.dashboard_home, name='home'),

    # Gallery
    path('dashboard/gallery/', views.gallery_list, name='gallery'),
    path('dashboard/gallery/<int:pk>/delete/', views.gallery_delete, name='gallery_delete'),

    # Events
    path('dashboard/events/', views.event_list, name='events'),
    path('dashboard/events/new/', views.event_create, name='event_create'),
    path('dashboard/events/<int:pk>/edit/', views.event_edit, name='event_edit'),
    path('dashboard/events/<int:pk>/delete/', views.event_delete, name='event_delete'),

    # Projects
    path('dashboard/projects/', views.project_list, name='projects'),
    path('dashboard/projects/new/', views.project_create, name='project_create'),
    path('dashboard/projects/<int:pk>/edit/', views.project_edit, name='project_edit'),
    path('dashboard/projects/<int:pk>/delete/', views.project_delete, name='project_delete'),
]