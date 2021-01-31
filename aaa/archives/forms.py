from home.forms import CreatePostForm, Custommmf, Tag
from django import forms
from home.models import PostLink
from home.mixins import ValidateLinkMixin
from .models import LecturePost
from accounts.models import ProfileDetail
import bleach, datetime
from django.contrib.admin import widgets
from django.shortcuts import redirect
from django.contrib import messages
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
        fields = ['heading','content', 'img', 'pdf_name', 'pdf']

    def __init__(self, request=None, pk=None,conference=None,*args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['heading'].widget = forms.Textarea(attrs={ "cols":20, "style": "height:150px; width:95%; border:2px outset white;"})
        if conference:
            self.fields['heading'].widget.attrs['placeholder'] = 'Conference Heading'
        else:
            self.fields['heading'].widget.attrs['placeholder'] = 'Lecture Heading'
        self.conference = conference
        self.request = request


    def save(self, commit=True):
        saveobj = super().save(commit=False)
        if self.request.user.is_staff:
            saveobj.user = self.request.user
            print('oh yess oh yaa.')
            if self.conference:
                saveobj.conference = True
            else:
                saveobj.lecture = True
            try:
                lecture_start_date =  self.request.POST.get('lecture_start_date').split(':')
                lecture_start_date = ' '.join(lecture_start_date)
                lecture_start_date = datetime.datetime.strptime(lecture_start_date, "%d %B %Y %H %M %p")
                print(lecture_start_date)
                saveobj.lecture_start_date = lecture_start_date

                lecture_end_date = self.request.POST.get('lecture_end_date').split(':')
                lecture_end_date = ' '.join(lecture_end_date)
                lecture_end_date = datetime.datetime.strptime(lecture_end_date, "%d %B %Y %H %M %p")

                saveobj.lecture_end_date = lecture_end_date
            except Exception as e:
                messages.error(self.request, 'Enter valid lecture start and end dates.', extra_tags = self.request.user.email)
                return redirect('archives:createconference')


        if commit:
            saveobj.save()
        print('yay saved \n\n\n')
        print(saveobj.lecture_start_date)
        print(saveobj.lecture)
        if self.conference:
            try:
                tag = Tag.objects.get(name = 'Conferences')
                saveobj.tag.add(tag)
            except Exception as e:
                tag = Tag.objects.create(name = 'Conferences')
                saveobj.tag.add(tag)
        linkdict = self.clean_links()
        if linkdict:
            if linkdict['linkobj']:
                [saveobj.link.add(i) for i in linkdict['linkobj']]
        print(saveobj)
        [saveobj.tag.add(i) for i in self.cleaned_data['tag']]

        return saveobj
