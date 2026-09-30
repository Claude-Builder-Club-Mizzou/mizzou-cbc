"""
URL configuration for mizzou_cbc project.
"""
from django.conf import settings
from django.contrib import admin
from django.urls import include, path, re_path
from django.views.static import serve

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('landing.urls')),
    path('cb-exec/', include('dashboard.urls')),

    # Serve uploaded media (the GCS bucket mounted at MEDIA_ROOT) in production too.
    # django.conf.urls.static.static() only works when DEBUG=True, so use serve() directly.
    re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
]