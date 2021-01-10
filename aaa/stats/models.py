from django.db import models
from accounts.models import User
# Create your models here.
class RequestObj(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    ip = models.CharField(blank=True, max_length=100)
    headers = models.CharField(blank=True, max_length=10000)
    # TODO: Define fields here
