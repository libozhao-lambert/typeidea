from django.shortcuts import render
from django.http import HttpResponse


# Link function views.
def links(request):
    return HttpResponse('links')
