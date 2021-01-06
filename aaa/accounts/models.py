from django.db import models
import datetime, sys
from datetime import date, timedelta
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
from django.conf import settings
from PIL import Image
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile

class UserManager(BaseUserManager):
    def create_user(self, email,username, password = None):
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
        )

        user.set_password(password)
        user.save(using=self._db)
        return user
    def create_staff(self, email, username, password):
        user = self.create_user(
            email = email,
            password=password,
            username = username,
        )
        user.staff = True

        user.save(using=self._db)
        return user
    def create_superuser(self, email, username, password):
        user = self.create_user(
            email = email,
            password=password,
            username = username,
        )
        user.admin = True
        user.staff = True
        user.is_active = True
        user.username = username
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    email = models.EmailField(max_length =255, unique = True)
    username = models.CharField(max_length = 20)
    reset = models.CharField(max_length=10000,blank=True,null=True)
    is_active = models.BooleanField(default = True)
    staff = models.BooleanField(default = False)
    admin = models.BooleanField(default = False)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    objects = UserManager()
    def __str__(self):
        try:
            return self.email
        except:
            return 'some prob in user object'
    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    def get_profile_name(self):
        if self.profile.name:
            return self.profile.name
        else:
            return self.username

    @property
    def is_staff(self):
        return self.staff

    @property
    def is_admin(self):
        return self.admin

    @property
    def get_email(self):
        return self.email

    @property
    def save_profile(self):
        usr = User.objects.get(email=self.email)
        prof=Profile.objects.create(user=usr,name=usr.username)
        for i in ['personal statement', 'experience','education','recommendation', 'accomplishments', 'interests']:
            a = ProfileDetail.objects.create(heading=i, details='')
            prof.details.add(a)
        prof.save()
        return prof

class MedicalCollege(models.Model):
    name = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        try:
            if self.name:
                return self.name
        except:
            return 'some prob in medical college object'

        else:
            return 'yet to be filled ' + str(self.pk)

class Degree(models.Model):
    name = models.ForeignKey('home.Tag',on_delete=models.SET_NULL, blank=True, null=True)
    college=models.ForeignKey(MedicalCollege, on_delete=models.SET_NULL, blank=True, null=True)
    finalyear=models.DateField(blank=True, null=True)
    def __str__(self):
        try:
            if self.name:
                return self.name.name
            else:
                return 'yet to be filled ' + str(self.pk)
        except:
            return 'some problem with degree object'
    def get_name(self):
        if self.name:
            a = self.name
            if a.name:
                return a.name
            else:
                return str(a.pk)
        else:
            return str(self.pk)

    def get_college(self):
        if self.college:
            a = self.college
            if a.name:
                return a.name
            else:
                return str(a.pk)
        else:
            return str(self.pk)

class Work(models.Model):
    position = models.CharField(max_length=50, null=True, blank=True)
    hospital = models.ForeignKey(MedicalCollege, on_delete=models.SET_NULL, blank=True, null=True)
    is_current = models.BooleanField(default=False)
    def __str__(self):
        try:
            if self.position:
                return self.position
            else:
                return 'yet to add' + str(self.pk)
        except:
            return 'some problem with work object'




class ProfileDetail(models.Model):
    heading=models.CharField(max_length=50, blank=True, null=True)
    details= models.CharField(max_length=1500, blank=True, null=True)
    pdf = models.FileField(blank=True, null=True, upload_to='cv/pdf/%Y/%m/$D/')
    def __str__(self):
        try:
            if self.heading:
                return self.heading
            else:
                return 'yet to add' + str(self.pk)
        except:
            return 'some problem with profile detail object'








class Profile(models.Model):
    user = models.OneToOneField(User,on_delete=models.SET_NULL, null=True, blank=True)
    profilepic = models.ImageField(blank=True, null = True, upload_to = 'profilepic/%Y/%m/$D/')
    backgroundpic = models.ImageField(blank=True, null = True, upload_to = 'backgroundpic/%Y/%m/$D/')
    name = models.CharField(max_length=50, null=True, blank=True)
    dob = models.DateField(blank=True, null=True)
    nationality = models.CharField(max_length=50, null=True, blank=True)
    links = models.ManyToManyField('home.PostLink', blank=True)
    phone = models.CharField(max_length=10, blank=True, null=True)
    degree = models.ManyToManyField(Degree, blank=True)
    details=models.ManyToManyField(ProfileDetail, blank=True)
    work = models.ManyToManyField(Work, blank=True)

    def __str__(self):
        try:
            if self.user.email:
                return self.user.email
            else:
                return str(self.pk)
        except:
            return 'some problem in getting user'

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
        if self.backgroundpic:
            self.backgroundpic = self.compressImage(self.backgroundpic)
        if self.profilepic:
            self.profilepic = self.compressImage(self.profilepic)
        super(Profile, self).save(*args, **kwargs)

    def get_work(self):
        a = self.work.all()
        if a:
            return list(a)

        else:
            return False
    def current_work(self):
        a = self.get_work()
        current = []
        if a:
            for work in a:
                if work.is_current:
                    current.append(work)
                else:
                    pass
            return current
        else:
            return False


    def get_personal(self):
        a = {}
        a['name'] = self.name
        a['dob'] = self.dob
        a['nationality'] = self.nationality
        if a:
            return a
        else:
            return False

    def get_links(self):
        a = self.links.all()
        print(a)
        if len(a) < 2:
            return list(a)
        else:
            return a
    def get_contact(self):
        a= {}
        a['email'] = self.user.email
        a['phone']=self.phone
        a['links']=self.get_links()
        return a

    def get_degrees(self):
        d = list(self.degree.all())
        if len(d) >= 1:
           return d
        else:
            return False
    def get_details(self):
        d= list(self.details.all())
        if len(d) >= 1:
            return d
        else:
            return False

    def list_heading(self):
        d = self.get_details()
        e=[]
        for i in d:
            e.append(i.heading)
        return e
    def get_backgroundpic(self):
        try:
            a = self.profilepic
            return a
        except:
            return False

    def get_profilepic(self):
        try:
            a = self.backgroundpic
            return a
        except:
            return False
