from django.urls import path
from . import seo, views

urlpatterns = [
    path('llms.txt', seo.llms_txt, name='llms_txt'),
    path('robots.txt', seo.robots_txt, name='robots_txt'),
    path('sitemap.xml', seo.sitemap_xml, name='sitemap'),
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('gallery/', views.gallery, name='gallery'),
    path('benefits/', views.benefits, name='benefits'),
    path('team/', views.team, name='team'),
    path('projects/', views.projects, name='projects'),
    # Not under projects/ so a project titled "Submit" can't shadow it.
    path('submit-project/', views.submit_project, name='submit_project'),
    path('submit-project/thanks/', views.submit_thanks, name='submit_thanks'),
    path('projects/<slug:slug>/', views.project_detail, name='project_detail'),
    path('builders/<slug:slug>/', views.builder_detail, name='builder_detail'),
    path('connect/', views.connect, name='connect'),
]
