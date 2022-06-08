from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static

urlpatterns = [
    path('', include('courses.urls'), name='main'),
    path('admin/', admin.site.urls, name='admin'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if 'rosetta' in settings.INSTALLED_APPS:
    urlpatterns += [
        path('rosetta/', include('rosetta.urls'))
    ]
