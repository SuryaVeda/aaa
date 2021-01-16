from django.shortcuts import render
from django.views.generic import TemplateView
from .models import Notification
from archives.models import LecturePost
# Create your views here.
class ShowNotification(TemplateView):
    template_name = 'home/notifications.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        notif = Notification.objects.filter(user=self.request.user).order_by('date')
        lectures = []
        posts = []
        for i in notif:
            if i.post and i.post.lecture:
                lectures.append(LecturePost.objects.get(pk=i.post.pk))
            else:
                posts.append(i.post)

        context['posts'] = posts
        context['lectures'] = lectures
        print(posts)
        print(lectures)
        return context
