from django.db import models
from accounts.models import User, Profile
from home.models import Tag, PostLink
from django.utils import timezone
from PIL import Image
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.core.files import File
import sys,os, datetime


# Create your models here.




class Book(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    subject = models.ForeignKey('home.Tag', on_delete=models.SET_NULL, null=True, blank=True)
    name = models.CharField(max_length=100, blank=True, null=True)
    links = models.ManyToManyField('home.PostLink', blank=True)
    latest = models.CharField(max_length=30, blank=True, null=True)
    backgroundPic = models.ImageField(blank=False, null=True, upload_to='bookimages/%Y/%m/$D/')
    def __str__(self):
        if self.name:
            return self.name
        elif self.user:
            return self.user.username
        else:
            return str(self.pk)
    def get_subject_name(self):
        if self.subject:
            return self.subject.name
        else:
            return 'subject not added'
    def compressImage(self, image):
        im = Image.open(image)
        output = BytesIO()
        im = im.resize((900, 600))
        im.save(output, format='JPEG', quality=60)
        output.seek(0)
        newimage = InMemoryUploadedFile(output, 'ImageField', '%s.jpg' % image.name.split('.')[0], 'image/jpeg',
                                        sys.getsizeof(output), None)
        return newimage

    def save(self, *args, **kwargs):
        if self.backgroundPic:
            self.backgroundPic = self.compressImage(self.backgroundPic)
        super(Book, self).save(*args, **kwargs)



    def get_source_link(self):
        a = []
        if self.links:
            l = list(self.links.all())
            for i in l:
                a.append((i.link_name, i.link))
            return a
        else:
            return False

    def get_reviews(self):
        a= self.review_set.all()
        if a:
            return list(a)
        else:
            return False











class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    book = models.ForeignKey(Book, on_delete=models.SET_NULL, null=True, blank=True)
    date = models.DateTimeField(default=timezone.make_aware(datetime.datetime.now(), timezone.get_default_timezone()))
    details = models.CharField(max_length=2000, blank=True, null=True)

    def __str__(self):
        if self.details:
            return self.details
        elif self.user:
            return self.user.username
        else:
            return str(self.pk)

    def post_details(self):
        if self.user and self.date:
            return '{0} | {1}'.format('Group Admin', self.date.strftime('%d %b %Y %I %M %p'))
        else:
            return 'Anonymous User'
