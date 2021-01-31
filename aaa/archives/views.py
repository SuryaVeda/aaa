from django.shortcuts import render, redirect
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView, CreateView, UpdateView, DeleteView
from .models import *
from home.decorators import staff_required
from accounts.models import User, Profile, ProfileDetail
from home.models import  Tag, PostLink
from .forms import *
import bleach, datetime,pytz
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError
from django.contrib import messages
from django.core.files.storage import FileSystemStorage
from .models import LecturePost
from accounts.models import ProfileDetail
from django.core.mail import send_mail
from django.conf import settings

# Create your views here.


class LecturePage(TemplateView):
    template_name = 'archives/hello.html'

    @method_decorator(staff_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        utc = pytz.UTC
        tz = pytz.timezone('Asia/Kolkata')
        today = datetime.datetime.now(tz)
        x = []
        y = []
        for i in LecturePost.objects.filter(lecture=True).order_by('-pk'):
            if utc.localize(i.lecture_start_date) > today:
                x.append(i)
            else:
                y.append(i)
        context['lectures'] = x
        context['pastlectures'] = y
        tag_speciality = Tag.objects.filter(is_speciality=True)
        context['tag_speciality'] = list(tag_speciality)
        print(context)
        return context

class ConferencePage(TemplateView):
    template_name = 'home/conference.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tag = Tag.objects.get(name='Conferences')
        context['oldposts'] = Post.objects.filter(tag=tag, conference=False).order_by('-pk')
        tag_speciality = Tag.objects.filter(is_speciality=True)
        context['tag_speciality'] = list(tag_speciality)
        context['posts'] = LecturePost.objects.filter(tag=tag, conference=True).order_by('lecture_start_date')
        return context

class LecturePostCreateView(CreateView):
    model = LecturePost
    form_class = LecturePostForm
    success_url = '/'
    def get_template_names(self):
        if self.request.GET.get('createconference'):
            template_name = 'home/conferenceForm.html'
        else:
            template_name = 'home/lectureform.html'
        return template_name

    def get(self, request, *args, **kwargs):
        if not request.GET.get('createconference'):
            self.kwargs['conference'] = None
        return super().get(request, *args, **kwargs)
    def post(self, *args, **kwargs):
        if self.request.POST.get('conferencebtn'):
            self.kwargs['conference'] = True
        else:
            self.kwargs['conference'] = False
        return super().post(self.request, *args, **kwargs)
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update(request=self.request)
        kwargs.update(self.kwargs)
        return kwargs
    def get_success_url(self):
        if self.kwargs['conference']:
            return reverse('home:conf')
        return reverse('archives:lectures')
class ProfileDetailUpdateView(UpdateView):
    model = ProfileDetail
    form_class = ProfileDetailForm
    success_url = '/'
    template_name = 'home/profiledetailsform.html'
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update(request=self.request)
        kwargs.update(self.kwargs)
        kwargs.update(obj = LecturePost.objects.get(pk=kwargs['opk']))
        return kwargs
    def get_success_url(self):
        return reverse('archives:lectures')
class ProfileDetailCreateView(CreateView):
    model = ProfileDetail
    form_class = ProfileDetailForm
    success_url = '/'
    template_name = 'home/profiledetailsform.html'
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update(request=self.request)
        kwargs.update(self.kwargs)
        kwargs.update(obj = LecturePost.objects.get(pk=kwargs['opk']))
        return kwargs
    def get_success_url(self):
        return reverse('archives:lectures')

class LecturePostUpdateView(UpdateView):
    model = LecturePost
    form_class = LecturePostForm
    success_url = '/'
    template_name = 'home/lectureform.html'
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update(request=self.request)
        kwargs.update(self.kwargs)
        return kwargs
    def get_success_url(self):
        return reverse('archives:lectures')




class PostLinkUpdateView(UpdateView):
    model = PostLink
    template_name = 'home/linkform.html'
    form_class = PostLinkForm
    success_url = '/'
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update(request=self.request)
        kwargs.update(self.kwargs)
        kwargs.update(obj = LecturePost.objects.get(pk=kwargs['opk']))
        return kwargs
    def get_success_url(self):
        return reverse('archives:lectures')
class PostLinkDeleteView(DeleteView):
    model = PostLink
    template_name = None

class ArchivePage(TemplateView):
    template_name = 'home/archie.html'

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated and request.user.is_staff:
            return render(request, self.template_name, self.get_context_data())
        else:
            return redirect('home:stafferror')
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tag_speciality'] = Tag.objects.filter(is_speciality=True)
        return context

class CleanLinkMixin:
    def assign_links(self):
        link_name = self.request.POST.getlist('link_name')
        link = self.request.POST.getlist('link')
        if len(link_name) != len(link) or len(link_name)==0:
            return False
        else:
            return list(zip(link_name, link))

    def clean_links(self, **kwargs):
        newdic = {}
        newdic['links'] = []
        if self.assign_links():
            for i in self.assign_links():
                if i:
                    validator = URLValidator()
                    link_name = bleach.clean(i[0], strip=True)
                    try:
                        validator(i[1])
                        link = i[1]
                        newdic['links'].append([link_name, link])

                    except ValidationError:
                        print('url not valid')
                        messages.error(self.request, 'Kindly enter valid Url ')
                        return False
            objlist = self.create_links(newdic)
            if objlist:
                return objlist
            else:
                return False

        else:
            return False
    def create_links(self, newdic):
        objlist =[]
        if newdic:
            print(newdic)
            for key in newdic:
                if key and newdic[key]:
                    for linkobj in newdic[key]:
                        print(linkobj)
                        try:
                            a = PostLink.objects.get(link_name = linkobj[0], link=linkobj[1])
                            objlist.append(a)
                            print('link obj already presetn')
                        except:
                            a = PostLink.objects.create(link_name = linkobj[0], link=linkobj[1])
                            a.user = self.request.user
                            a.save()
                            print('link object created')
                            objlist.append(a)
                    return objlist
                else:
                    return False


        else:
            return False


class CleanTextMixin:
    def clean_text(self, a):
        newdic = {}
        if a:
            print(a)
            for i in a:

                tagtext = bleach.clean(self.request.POST.get(i), strip=True)
                if i == 'subjecttag':
                    try:
                        x = Tag.objects.get(name=tagtext, is_degree=True)
                        newdic[i] = x
                    except:
                        messages.error(self.request, 'Kindly enter valid tag ')
                        return False

                else:
                    newdic[i] = tagtext


            return newdic

        else:
            messages.error(self.request, 'Kindly enter text ')
            return False

class CleanImageMixin:

    def image_valid(self, *args):
        valid_extensions = ['jpeg', 'png', 'jpg']
        if args:
            for i in args:
                if not i:
                    return False
                print(i.name.split('.'))
                if len(i.name.split('.')) > 2:
                    messages.error(self.request, 'enter valid image')
                    return False
                else:
                    if i.name.split('.')[1] in valid_extensions:
                        print('yes image has valid extension')
                        if self.validate_image_size(i):
                            return i
                        else:
                            return False
                    else:
                        print('not valid extension')
                        return False

        else:
            return False

    def validate_image_size(self, a):
        if a.size / 1024 / 1024 > 5:
            messages.error(self.request, 'image size greater than 5 mb')
            return False
        else:
            return True








class BookFormMixin(CleanImageMixin,CleanLinkMixin,CleanTextMixin):

    def save_book_form(self):

        textlist = ['book_name', 'subjecttag', 'latest', 'review']

        link_list = self.clean_links()
        text_dict = self.clean_text(textlist)
        image = self.image_valid(self.request.FILES.get('image'))

        if text_dict:
            print('all fields are entered correctly')
            a = Book.objects.create(name=text_dict['book_name'], latest=text_dict['latest'])
            a.user = self.request.user
            a.subject = text_dict['subjecttag']
            if image:
                storage = FileSystemStorage()
                filename = storage.save(image.name, image)
                with storage.open(filename) as f:
                    a.backgroundPic.save(filename, f, save=True)

            if link_list:
                for i in link_list:
                    a.links.add(i)

            a.save()
            x = Review.objects.create(user=self.request.user, book=a, date=timezone.make_aware(datetime.datetime.now(), timezone.get_default_timezone()), details=text_dict['review'])
            return text_dict['subjecttag']


        else:
            messages.error(self.request, 'kindly fill form accurately')

    def edit_book_form(self):

        textlist = ['book_name', 'subjecttag', 'latest', 'review']

        link_list = self.clean_links()
        text_dict = self.clean_text(textlist)
        image = self.image_valid(self.request.POST.get('image'))

        if text_dict:
            print('successfull')
            a = Book.objects.get(pk=int(self.request.POST.get('bookformbtn')))

            a.name = text_dict['book_name']
            a.latest = text_dict['latest']
            a.subject = text_dict['subjecttag']
            if link_list:
                for i in link_list:
                    a.links.add(i)
            if image:
                storage = FileSystemStorage()
                filename = storage.save(image.name, image)
                with storage.open(filename) as f:
                    a.backgroundPic.save(filename, f, save=True)

            a.save()
            print(a.name)
            print(a.subject.name)
            try:
                x = Review.objects.get(user=self.request.user, book=a)
                x.date= timezone.now()
                x.details = text_dict['review']
                x.save()
            except:
                x= Review.objects.create(user=self.request.user, book=a, date=timezone.make_aware(datetime.datetime.now(), timezone.get_default_timezone()), details=text_dict['review'])
            return text_dict['subjecttag']

        else:
            messages.error(self.request, 'kindly fill form accurately')
            return False



class ArchDetail(BookFormMixin,TemplateView):

    template_name = 'home/archdetail.html'

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated and request.user.is_staff:
            return render(request, self.template_name, self.get_context_data())
        else:
            return redirect('home:stafferror')
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['subjects'] = list(Tag.objects.filter(is_degree = True, is_speciality = False))+ list(Tag.objects.filter(is_speciality = True))
        context['books'] = Book.objects.all()
        context['tag_speciality'] = Tag.objects.filter(is_speciality=True)
        try:
            a = Review.objects.filter(user=self.request.user)
            if a:
                b = True
            else:
                b = False
        except:
            b=False

        context['has_review'] = b
        return context

    def post(self, *args, **kwargs):
        if self.request.user.is_authenticated and self.request.user.is_staff:
            print(self.request.POST)
            print(self.request.POST.get('image'))
            if self.request.POST.get('addbookformbtn'):
                subject = self.save_book_form()
                return redirect('/home/{0}'.format(subject))
            if self.request.POST.get('bookformbtn'):
                subject = self.edit_book_form()
                return redirect('/home/{0}'.format(subject))
            return redirect('home:home')

        else:
            return redirect('home:stafferror')




class Test(TemplateView):
    template_name = 'home/test.html'

    def post(self, *args, **kwargs):
        x = Book.objects.get(name= 'a')



        return redirect('archives:test')

def delete_book_view(request, pk):
    if pk and request.user.is_authenticated and request.user.is_admin:
        try:
            x = Book.objects.get(pk=pk)
            if x.user == request.user or request.user.is_admin:
                x.delete()
            else:
                messages.error(request, 'not a valid user')

            return redirect('home:home')
        except:
            messages.error(request, 'Book doesnot exist')
            return redirect('home:home')
    else:
        return ('home:stafferror')

def delete_post_detail(request, pk):
    if pk and request.user.is_authenticated and request.user.is_admin:
        try:
            x = ProfileDetail.objects.get(pk=pk)
            x.delete()
            return redirect('archives:lectures')
        except:
            messages.error(request, 'Book doesnot exist')
            return redirect('home:home')
    else:
        return ('home:stafferror')
def delete_review_view(request, pk):
    if pk and request.user.is_authenticated and request.user.is_admin:
        try:
            x = Review.objects.get(pk=pk)
            if x.user == request.user or request.user.is_admin:
                x.delete()
            else:
                messages.error(request, 'not a valid user')

            return redirect('home:home')
        except:
            messages.error(request, 'Book doesnot exist')
            return redirect('home:home')
    else:
        return ('home:stafferror')
@staff_required
def send_mail_view(request, pk):
    post = LecturePost.objects.get(pk=pk)
    messagelist = []
    if post.get_links:
        for i in post.get_links():
            messagelist.append(i.link_name)
            messagelist.append(i.link)
            messagelist.append('\n')
    message = " ".join(messagelist)
    send_mail("Below are the links related to lecture.", "Kindly press the below link or copy and paste it in browser to join the lecture \n \n {0}".format(message), settings.EMAIL_HOST_USER, [request.user.email], fail_silently=True)
    messages.success(request,'Email sent successfully', extra_tags=request.user.email)
    return redirect('archives:lectures')
