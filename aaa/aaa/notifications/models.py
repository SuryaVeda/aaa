from django.db import models
from accounts.models import User
from home.models import Post
# Create your models here.
class Notification(models.Model):
    date = models.DateTimeField(auto_now_add=True,auto_now=False, null=True)
    user = models.ForeignKey(User,on_delete= models.SET_NULL, null = True, blank = True)
    post = models.ForeignKey(Post,on_delete= models.SET_NULL, null = True, blank = True)
    message = models.CharField(null=True,blank=True, default='New message', max_length=100)
    def __str__(self):
        return self.message
