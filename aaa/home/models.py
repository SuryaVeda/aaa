from django.db import models
from urllib.parse import urlparse, parse_qs
import datetime
from PIL import Image
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile
import sys,os
from django.utils import timezone
from accounts.models import User

# Create your models here.
print(os.getcwd())


class ImageAdd(models.Model):
    user = models.ForeignKey(User, on_delete= models.SET_NULL, null = True, blank = True )
    name = models.CharField(max_length=20, blank=True, null=True)
    img = models.ImageField(blank=True, null = True, upload_to = 'contentfeedImages/%Y/%m/$D/')

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
        if self.img:
            self.img = self.compressImage(self.img)
        super(ImageAdd, self).save(*args, **kwargs)

class PostLink(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    link= models.URLField(blank=True, null=True, max_length=400)
    link_name = models.CharField(blank=True, null=True, max_length=50)
    def __str__(self):
        return self.link_name

class Tag(models.Model):
    name = models.CharField(max_length=40, blank=True, null=True)
    is_speciality=models.BooleanField(default=False)
    is_degree = models.BooleanField(default=False)
    details=models.ManyToManyField('accounts.ProfileDetail', blank=True)

    @property
    def get_questions(self):
        try:
            return self.questionbank_set.all()
        except:
            return False
    @property
    def get_details(self):
        d = list(self.details.all().order_by('pk'))
        if len(d) >= 1:
            return d
        else:
            return False
    def __str__(self):
        try:
            if self.name:
                return self.name
            else:
                return str(self.pk)
        except:
            return 'some problem in tag object'

    def get_books(self):
        if self.is_degree:
            a = self.book_set.all()
            if a:
                return list(a)
            else:
                return False
        else:
            return False

class Comment(models.Model):
    date = models.DateTimeField(default=timezone.make_aware(datetime.datetime.now(), timezone.get_default_timezone()))
    user = models.ForeignKey(User, on_delete= models.SET_NULL, null = True, blank = True )
    text = models.TextField(max_length=500, blank=True, null=True)
    img = models.ImageField(blank=True, null = True, upload_to = 'commentimages/%Y/%m/$D/')
    link = models.ManyToManyField(PostLink, blank=True, null=True)
    pdf = models.FileField(blank=True, null=True, upload_to='commentsPosts/pdf/%Y/%m/$D/')
    pdf_name = models.CharField(blank=True, null=True, max_length=50)
    def __str__(self):
        try:
            if self.text:
                return self.text
            else:
                return 'no text added'
        except:
            return 'some problem in comment object'

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
        if self.img:
            self.img = self.compressImage(self.img)
        super(Comment, self).save(*args, **kwargs)

    def get_images(self):
        a = self.img.all()
        if len(a) < 2:
            return list(a)
        else:
            return a

    def get_links(self):
        a = self.link.all()
        if len(a) < 2:
            return list(a)
        else:
            return a

    def posted_on(self):
        return self.date.strftime('%d %b %Y %I %M %p')


class Post(models.Model):
    date = models.DateTimeField(auto_now_add=True,auto_now=False, null=True)
    user = models.ForeignKey(User, on_delete= models.SET_NULL, null = True, blank = True )

    heading = models.CharField(max_length=1000, null=False, blank=False)
    img = models.ImageField(blank=True, null=True, upload_to='Postimages/%Y/%m/$D/')
    link = models.ManyToManyField(PostLink, blank=True, null=True)
    pdf = models.FileField(blank=True, null=True, upload_to='homePosts/pdf/%Y/%m/$D/')
    pdf_name = models.CharField(blank=True, null=True, max_length=50)
    content=models.CharField(max_length=1000,blank=True, null=True)
    comments = models.ManyToManyField(Comment, blank=True, null=True)
    tag = models.ManyToManyField(Tag)
    def __str__(self):
        try:
            if self.heading:
                return self.heading
            elif self.user:
                return self.user.username
            elif self.date:
                return self.posted_on
            else:
                return 'no heading'
        except:
            return 'some problem in post object'

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
        if self.img:
            self.img = self.compressImage(self.img)
        super(Post, self).save(*args, **kwargs)
    def get_comments(self):
        a = self.comments.all()
        if len(a) < 2:
            return list(a)
        else:
            return a
    def get_tags(self):
        a = self.tag.all()
        if len(a) < 2:
            return list(a)
        else:
            return a



    def get_links(self):
        a = self.link.all()
        if len(a) < 2:
            return list(a)
        else:
            return a

    @property
    def posted_on(self):

        try:
            #x = '{0}  |  {1} '.format(self.user.username, self.date.strftime('%d %b %Y %I %M %p'))
            x = '{0}  |  {1} '.format('Admin', self.date.strftime('%d %b %Y %I %M %p'))

            return x
        except:
            return 'Group Admin'
