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

    # Submissions (public project submissions awaiting review)
    path('dashboard/submissions/', views.submission_list, name='submissions'),
    path('dashboard/submissions/<int:pk>/approve/', views.submission_review, {'decision': 'approve'}, name='submission_approve'),
    path('dashboard/submissions/<int:pk>/reject/', views.submission_review, {'decision': 'reject'}, name='submission_reject'),
    path('dashboard/submissions/<int:pk>/delete/', views.submission_delete, name='submission_delete'),

    # Builders
    path('dashboard/builders/', views.builder_list, name='builders'),
    path('dashboard/builders/new/', views.builder_create, name='builder_create'),
    path('dashboard/builders/<int:pk>/edit/', views.builder_edit, name='builder_edit'),
    path('dashboard/builders/<int:pk>/delete/', views.builder_delete, name='builder_delete'),

    # Team
    path('dashboard/team/', views.team_list, name='team'),
    path('dashboard/team/new/', views.team_create, name='team_create'),
    path('dashboard/team/<int:pk>/edit/', views.team_edit, name='team_edit'),
    path('dashboard/team/<int:pk>/delete/', views.team_delete, name='team_delete'),
]
