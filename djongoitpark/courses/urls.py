from django.urls import path
from django.views.generic import TemplateView

from . import views

app_name = 'courses'

urlpatterns = [
    path('dashboard/', views.index, name='home'),
    path('shortener/', TemplateView.as_view(template_name='courses/form.html'), name='shortener'),
    path('<str:slug>', views.ExternalLinksView.as_view(), name='home'),
]
