from django.db import models
from accounts.models import User
from home.models import Post
import pytz, datetime
from django.utils import timezone
# Create your models here.





class Notification(models.Model):
    user = models.OneToOneField(User,on_delete= models.SET_NULL, null = True, blank = True)
    message = models.ManyToManyField('notifications.Message')
    count = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return self.user.email

class Message(models.Model):
    date = models.DateTimeField(auto_now_add=True,auto_now=False, null=True)
    text = models.CharField(blank=True,null=True, max_length=200)
    post_url = models.URLField(blank=True, null=True)
    type = models.CharField(blank=True,null=True, max_length=100)
    read = models.BooleanField(default=False, null = True)
    def create_notifications(self):
        users = list(Users.objects.filter(staff= True))
        for user in users:
            if user.notification:
                pass
            else:
                pass
        return 'hello'
