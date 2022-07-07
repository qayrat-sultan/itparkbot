from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.views.generic import TemplateView

urlpatterns = [
    path("", TemplateView.as_view(template_name="home.html"), name="home"),
    path('go/', include('courses.urls'), name='main'),
    path('administration/', admin.site.urls, name='admin'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if 'rosetta' in settings.INSTALLED_APPS:
    urlpatterns += [
        path('rosetta/', include('rosetta.urls'))
    ]

admin.site.site_header = "IT Park Tashkent Admin"
admin.site.index_title = "Adminkaga xush kelibsiz"
admin.site.site_title = "Adminka tutoriali"
admin.site.index_template = 'admin/index.html'
admin.autodiscover()