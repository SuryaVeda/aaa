from django.db import models
from accounts.models import User
from home.models import Post
import pytz, datetime
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist
# Create your models here.





class Notification(models.Model):
    user = models.OneToOneField(User,on_delete= models.SET_NULL, null = True, blank = True)
    message = models.ManyToManyField('notifications.Message')
    count = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return self.user.email

class CustomManager(models.Manager):
    def delete_messages(self, url):
        x = super().get_queryset().filter(post_url = url)
        if x:
            x.delete()
        return True




class Message(models.Model):
    date = models.DateTimeField(auto_now_add=True,auto_now=False, null=True)
    text = models.CharField(blank=True,null=True, max_length=200)
    post_url = models.URLField(blank=True, null=True)
    type = models.CharField(blank=True,null=True, max_length=100)
    read = models.BooleanField(default=False, null = True)
    objects = CustomManager()
    def create_notifications(self, post_user):
        users = list(User.objects.filter(staff= True))
        for user in users:
            if user != post_user:
                try:
                    notification = user.notification
                    notification.count += 1
                    print(self)
                    notification.message.add(self)
                    notification.save()
                except ObjectDoesNotExist:
                    notification = Notification.objects.create(user = user, count = 0)
                    notification.count += 1
                    print(self)
                    notification.message.add(self)
                    notification.save()
        return 'hello'
