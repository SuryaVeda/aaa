from home.forms import CreatePostForm, Custommmf, Tag
from django import forms
from home.models import PostLink
from home.mixins import ValidateLinkMixin
from .models import LecturePost
from accounts.models import ProfileDetail
import bleach, datetime
from django.contrib.admin import widgets
from django.shortcuts import redirect

class ProfileDetailForm(forms.ModelForm):
    # TODO: Define other fields here

    class Meta:
        model = ProfileDetail
        fields = ['heading', 'details']

    def __init__(self,request = None, pk=None,obj=None, opk=None, *args, **kwargs):
        super(ProfileDetailForm, self).__init__(*args, **kwargs)
        self.fields['heading'].widget.attrs['placeholder'] = 'Add Heading for detail'
        self.fields['details'].widget.attrs['placeholder'] = 'Add Details'
        self.request = request
        self.obj = obj
        self.pk = pk

    def save(self,commit=True):
        print(self.request.POST)
        heading = self.request.POST.getlist('heading')
        details = self.request.POST.getlist('details')
        h1 = heading.pop(0)
        d1 = details.pop(0)
        try:
            prof = ProfileDetail.objects.get(pk=self.pk)
            prof.heading = h1
            prof.details = d1
            prof.save()
        except:
            prof = ProfileDetail.objects.create(heading = bleach.clean(h1, strip=True), details = bleach.clean(d1, strip=True))
            self.obj.post_details.add(prof)
        if len(heading) == len(details):
            for i,j in zip(heading, details):
                prof = ProfileDetail.objects.create(heading = bleach.clean(i, strip=True), details = bleach.clean(j, strip=True))
                self.obj.post_details.add(prof)

        print(heading)
        return self.obj.get_post_details

class PostLinkForm(forms.ModelForm,ValidateLinkMixin):
    class Meta:
        model = PostLink
        fields = ['link', 'link_name']
    def __init__(self, request=None,obj=None,pk=None,opk=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['link_name'].widget.attrs['placeholder'] = 'Add name for Link'
        self.fields['link'].widget.attrs['placeholder'] = 'Add link address'
        self.request = request
        self.obj=obj
    def save(self, commit=True):
        print(self.request.POST)
        linkdict = self.clean_links()
        if linkdict:
            if linkdict['linkobj']:
                self.obj.link.all().delete()
                [self.obj.link.add(i) for i in linkdict['linkobj']]
        print(linkdict)
        return linkdict['linkobj']


class LecturePostForm(CreatePostForm, ValidateLinkMixin):
    tag = Custommmf(
        queryset=Tag.objects.filter(is_speciality=True),
        widget=forms.CheckboxSelectMultiple
    )
    class Meta:
        model = LecturePost
        fields = ['heading','content', 'img', 'pdf_name', 'pdf', 'lecture_start_date', 'lecture_end_date']

    def __init__(self, request=None, pk=None,*args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['heading'].widget.attrs['placeholder'] = 'Lecture Heading'
        self.request = request
        self.fields['lecture_start_date'].widget = widgets.AdminDateWidget()
        self.fields['lecture_end_date'].widget = widgets.AdminTimeWidget()

    def save(self, commit=True):
        saveobj = super().save(commit=False)
        if self.request.user.is_staff:
            saveobj.user = self.request.user
        print(self.request.POST)
        try:
            dateobj = self.cleaned_data['lecture_start_date']
            saveobj.lecture_start_date = datetime.datetime(dateobj.year, dateobj.month, dateobj.day, int(self.request.POST.get('starthour')), int(self.request.POST.get('startmin')))
            saveobj.lecture_end_date = datetime.datetime(dateobj.year, dateobj.month, dateobj.day, int(self.request.POST.get('endhour')), int(self.request.POST.get('endmin')))

        except Exception as e:
            return redirect('home:home')
        if commit:
            saveobj.save()
        print(saveobj.lecture_start_date)
        print(saveobj.lecture_end_date)
        linkdict = self.clean_links()
        if linkdict:
            if linkdict['linkobj']:
                [saveobj.link.add(i) for i in linkdict['linkobj']]
        print(saveobj)
        [saveobj.tag.add(i) for i in self.cleaned_data['tag']]

        return saveobj
