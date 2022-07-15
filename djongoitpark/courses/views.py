from django.shortcuts import render, redirect
from django.views.generic import DetailView

from .models import ExternalLinks


def index(request):
    return render(request, 'courses/index.html')


def external(request, link):
    print('link: %s' % link)
    return render(request, 'courses/index.html', {'link': link})


class ExternalLinksView(DetailView):
    model = ExternalLinks
    template_name = 'courses/index.html'
    context_object_name = 'external_links'
    slug_field = 'url'


