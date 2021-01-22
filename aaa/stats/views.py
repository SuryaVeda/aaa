from django.shortcuts import render, redirect

from django.views.generic import TemplateView
from .models import RequestObj, PageObj
from accounts.models import User
import pytz,datetime
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
        users = [list(i.requestobj_set.filter(date = datetime.datetime.now(pytz.timezone('Asia/Kolkata'))))[0] for i in User.objects.all() if i.requestobj_set.filter(date = datetime.datetime.now(pytz.timezone('Asia/Kolkata')))]
        print(users)
        context['location'] = [[type(i.get_ip_details()), i.user.email] for i in users if i]
        exp = [[type(i.get_ip_details()), i.user.email] for i in users if i]
        print(exp)
        return context
