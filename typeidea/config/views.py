from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import ListView

from .models import Link
from blog.views import CommonViewMixin


# Link function views.
class LinksView(CommonViewMixin, ListView):
    queryset = Link.get_links()
    context_object_name = 'link_list'
    template_name = 'config/links.html'
