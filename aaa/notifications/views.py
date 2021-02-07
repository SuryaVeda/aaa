from django.shortcuts import render
from django.views.generic import TemplateView
from .models import Notification
from home.models import Tag
from django.utils.decorators import method_decorator
from home.decorators import staff_required
# Create your views here.


@method_decorator(staff_required, name = 'dispatch')
class ShowNotification(TemplateView):
    template_name = 'home/notifications.html'
    def get(self, request, *args, **kwargs):
        try:
            notif = Notification.objects.get(user=self.request.user)
        except Exception as e:
            notif = Notification.objects.create(user = self.request.user, count = 0)
        self.kwargs['count'] = notif.count
        notif.count = 0
        notif.save()

        return super().get(request, *args, **kwargs)
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tag_speciality = Tag.objects.filter(is_speciality=True)
        messages = list(self.request.user.notification.message.all())
        context['tag_speciality'] = list(tag_speciality)
        messages.reverse()
        context['new_notifications'] = messages[0:self.kwargs['count']]
        context['notifications'] = messages[self.kwargs['count']:]
        print(context)
        return context
