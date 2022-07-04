from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static

urlpatterns = [
    path('go/', include('courses.urls'), name='main'),
    path('', admin.site.urls, name='admin'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if 'rosetta' in settings.INSTALLED_APPS:
    urlpatterns += [
        path('rosetta/', include('rosetta.urls'))
    ]

admin.site.site_header = "IT Park Tashkent Admin"
admin.site.index_title = "Adminkaga xush kelibsiz"
admin.site.site_title = "Adminka tutoriali"
print(admin.site.index_template)
admin.site.index_template = 'admin/index.html'
print(admin.site.index_template)
admin.autodiscover()