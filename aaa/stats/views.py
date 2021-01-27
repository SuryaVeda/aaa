from django.shortcuts import render, redirect
from home.models import Tag
from django.views.generic import TemplateView
from .models import RequestObj, PageObj
from accounts.models import User
import pytz,datetime,json
# Create your views here.

class StatPage(TemplateView):
    template_name = 'stats/stat.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['request_count'] = RequestObj.objects.count_requests()

        context['page'] = PageObj.objects.most_requested_page()
        context['pages'] = PageObj.objects.order_by('-count')
        print(PageObj.objects.all().count())
        context['active_user'] = User.custom_objs.most_active_users()
        tag_speciality = Tag.objects.filter(is_speciality=True)
        context['tag_speciality'] = list(tag_speciality)
        context['location'] = []
        return context
