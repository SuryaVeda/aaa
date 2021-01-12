from django.shortcuts import render
from django.views.generic import TemplateView
from .models import Notification
# Create your views here.
class ShowNotification(TemplateView):
    template_name = 'home/notifications.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        notif = Notification.objects.filter(user=self.request.user).order_by('-date')
        context['posts'] = [i.post for i in notif if i.post]
        return context
