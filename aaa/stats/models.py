from django.db import models
from accounts.models import User
import datetime,pytz,requests, json
from urllib.parse import urljoin

# Create your models here.
class CountPages(models.Manager):
    def most_requested_page(self):
        tz = pytz.timezone('Asia/Kolkata')
        x = [[i.requestobj_set.filter(date = (datetime.datetime.now(tz)).date()).count(), i.url] for i in  super().get_queryset()]
        y = [i[0] for i in x]
        if y:
            index = y.index(max(y))
            return x[index]
        else:
            return None

class PageObj(models.Model):
    url = models.URLField(blank=True, null=True)
    count = models.IntegerField(blank=True, null=True)
    objects = CountPages()

class CountRequests(models.Manager):
    def count_requests(self):
        tz = pytz.timezone('Asia/Kolkata')
        return super().get_queryset().filter(date = (datetime.datetime.now(tz)).date()).count()


class RequestObj(models.Model):

    date = models.DateField(default=(datetime.datetime.now(pytz.timezone('Asia/Kolkata'))).date())
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    location = models.CharField(blank=True, max_length=10000)
    page = models.ForeignKey(PageObj, on_delete=models.SET_NULL, null=True, blank=True)
    objects = CountRequests()

    def get_ip_details(self):
        if self.location:
            url = urljoin('http://ip-api.com/json/', self.location)
            response = requests.get(url).json()
            print(response)
            if response['status'] == 'success':
                return response
            else:
                return None
        else:
            return None

    # TODO: Define fields here
