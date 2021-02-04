from django.db import models
from accounts.models import User
from PIL import Image
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile
import sys
from django.conf import settings
# from home.models import Tag
# Create your models here.

class QTag(models.Model):
    name = models.CharField(max_length=20, blank=False)
    subject = models.BooleanField(default=False)
    degree = models.BooleanField(default=False)
    def __str__(self):
        try:
            return self.name
        except:
            return 'some problem in tag object'
    @property
    def get_questions(self):
        try:
            return self.questionbank_set.all()
        except:
            return False

    @property
    def is_degree(self):
        if self.degree:
            return True
        else:
            return False

    @property
    def is_subject(self):
        if self.subject:
            return True
        else:
            return False


class QuestionBank(models.Model):
    tag = models.ManyToManyField('home.Tag', null=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    links = models.ManyToManyField('home.PostLink', blank=True)
    date = models.DateField(auto_now_add=True)
    question = models.CharField(max_length=1000000, blank=True, null=True)
    answer = models.CharField(max_length=1000000, blank=True, null=True)
    mcq = models.BooleanField(default=False)
    flashcard = models.BooleanField(default=False)
    qa = models.BooleanField(default=False)

    def __str__(self):
        try:
            return self.question
        except:
            return str(self.pk)
    def get_absolute_url(self):
        if settings.DEBUG:
            return 'http://127.0.0.1:8000/mcq/question/{}'.format(self.pk)
        else:
            return 'https://allaboutanaesthesia.co/mcq/question/{}'.format(self.pk)
    @property
    def get_subjects(self):
        try:
            return list(self.tag.filter(is_speciality=True))
        except:
            return 'some problem in saving tag'
    @property
    def get_tags(self):
        try:
            return self.tag.all()
        except:
            return 'some problem in saving tag'
    @property
    def is_mcq(self):
        if self.mcq:
            return True
        else:
            return False

    @property
    def is_qa(self):
        if self.qa:
            return True
        else:
            return False

    @property
    def is_flashcard(self):
        if self.flashcard:
            return True
        else:
            return False

    @property
    def get_question_image(self):
        try:
            x = self.qimage_set.get(qimage = True)
            return x.image.url
        except:
            return False

    @property
    def get_answer_image(self):
        try:
            x = self.qimage_set.get(aimage=True)
            return x.image.url
        except:
            return False


    @property
    def get_links(self):
        try:
            x= self.links.all()
            return list(x)
        except:
            return False

class Qimage(models.Model):
    qinstance = models.ForeignKey(QuestionBank, on_delete=models.SET_NULL, null =True, blank=True)
    image = models.ImageField(upload_to='Questionbank/', blank=True, null=True)
    aimage = models.BooleanField(default=False)
    qimage = models.BooleanField(default=False)

    def compressImage(self, image):
        im = Image.open(image)
        output = BytesIO()
        if im.mode != 'RGB':
            im = im.convert('RGB')
        im = im.resize((900, 600))
        im.save(output, format='JPEG', quality=60)
        output.seek(0)
        newimage = InMemoryUploadedFile(output, 'ImageField', '%s.jpg' % image.name.split('.')[0], 'image/jpeg',
                                        sys.getsizeof(output), None)
        return newimage

    def save(self, *args, **kwargs):
        if self.image:
            self.image = self.compressImage(self.image)
        super(Qimage, self).save(*args, **kwargs)
