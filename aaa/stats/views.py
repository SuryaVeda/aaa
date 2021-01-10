from django.shortcuts import render, redirect

from django.views.generic import TemplateView

# Create your views here.

class StatPage(TemplateView):
    template_name = 'stats/stat.html'
