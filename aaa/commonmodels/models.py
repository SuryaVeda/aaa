from django.db import models

# Create your models here.
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


class FileAdd(models.Model):
    file_name = models.CharField(max_length=20, blank=True, null=True)
    file = models.FileField(blank=True, null = True, upload_to = 'files/%Y/%m/$D/')
    is_image = models.BooleanField(default=False)

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
        if self.is_image:
            self.file = self.compressImage(self.file)
        super(FileAdd, self).save(*args, **kwargs)

class PostLink(models.Model):
    link= models.URLField(blank=True, null=True, max_length=400)
    link_name = models.CharField(blank=True, null=True, max_length=50)
    def __str__(self):
        return self.link_name


class Comment(models.Model):
    date = models.DateTimeField(default=timezone.make_aware(datetime.datetime.now(), timezone.get_default_timezone()))
    user = models.ForeignKey(User, on_delete= models.SET_NULL, null = True, blank = True )
    text = models.TextField(max_length=1000, blank=True, null=True)
    image = models.ImageField(blank=True, null = True, upload_to = 'commentimages/%Y/%m/$D/')
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
        if self.image:
            self.image = self.compressImage(self.image)
        super(Comment, self).save(*args, **kwargs)


    def posted_on(self):
        return'{0}  |  {1} '.format(self.user.username, self.date.strftime('%d %b %Y %I %M %p'))

class CTag(models.Model):
    tag_name = models.CharField(max_length=20, null=True, blank=True)
    subject = models.BooleanField(default=False, null=True)
    degree = models.BooleanField(default=False, null=True)
    def __str__(self):
        try:
            return self.tag_name
        except:
            return 'some problem in Tag with pk {0}'.format(self.pk)
    @property
    def get_questions(self):
        return self.questionbank_set.all()

    @property
    def get_mcqs(self):
        try:
            mcq_list = []
            for i in self.get_questions:
                if i.is_mcq:
                    mcq_list.append(i)
                else:
                    continue
            return mcq_list
        except:
            return False

    @property
    def get_flashcards(self):
        try:
            mcq_list = []
            for i in self.get_questions:
                if i.is_flashcard:
                    mcq_list.append(i)
                else:
                    continue
            return mcq_list
        except:
            return False

    @property
    def get_qa(self):
        try:
            mcq_list = []
            for i in self.get_questions:
                if i.is_qa:
                    mcq_list.append(i)
                else:
                    continue
            return mcq_list
        except:
            return False
    @property
    def get_posts(self):
        try:
            return list(self.post_set.filter('-pk'))
        except:
            return 'some problem in returning posts'


class CDetails(models.Model):
    detail_heading = models.CharField(max_length=20, null=True, blank=True)
    text = models.CharField(max_length=100000, null=True, blank=True)
    def __str__(self):
        return '{0}'.format(self.pk)



class CPost(models.Model):
    date = models.DateTimeField(auto_now_add=True,auto_now=False, null=True)
    user = models.ForeignKey(User, on_delete= models.SET_NULL, null = True, blank = True )
    post_heading = models.CharField(max_length=1000, null=True, blank=True)
    post_details = models.ManyToManyField(Details, blank=True)
    post_links = models.ManyToManyField(PostLink, blank=True)
    post_files = models.ManyToManyField(FileAdd, blank=True )
    post_comments = models.ManyToManyField(Comment, blank=True)
    post_tags = models.ManyToManyField(Tag, blank=True)
    def __str__(self):
        try:
            if self.post_heading:
                return self.post_heading
            elif self.user:
                return self.user.username
            elif self.date:
                return self.posted_on
            else:
                return 'no heading'
        except:
            return 'some problem in post object'



    @property
    def get_post_images(self):
        image_list = []
        for i in self.files.all():
            if i.is_image:
                image_list.append(i)
            else:
                continue
        return image_list

    @property
    def get_post_files(self):
        image_list = []
        for i in self.files.all():
            if not i.is_image:
                image_list.append(i)
            else:
                continue
        return image_list


    @property
    def get_post_details(self):
        return list(self.post_details.filter('-pk'))
    @property
    def get_comments(self):
        a = self.post_comments.filter('-pk')
        return list(a)
    @property
    def get_tags(self):
        a = self.post_tags.all()
        return list(a)
    @property
    def get_links(self):
        a = self.post_links.all()
        return list(a)

    @property
    def posted_on(self):
        try:
            x = '{0}  |  {1} '.format(self.user.username, self.date.strftime('%d %b %Y %I %M %p'))
            return x
        except:
            return 'Group Admin'





