"""
URL configuration for Dr. Saidi Kapiga Research Site
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('research.urls')),
    path('api/', include('research.api_urls')),
]

# Serve media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# Customize admin site
admin.site.site_header = "Dr. Saidi Kapiga Research Administration"
admin.site.site_title = "Research Admin"
admin.site.index_title = "HIV Research in Africa - Administrative Interface"
