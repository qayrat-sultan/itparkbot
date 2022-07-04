from django.urls import path
from . import views

app_name = 'courses'

urlpatterns = [
    path('dashboard/', views.index, name='home'),
    path('<str:slug>', views.ExternalLinksView.as_view(), name='home'),
]
