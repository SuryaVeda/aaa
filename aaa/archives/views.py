from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from .models import *
from accounts.models import User, Profile
from home.models import  Tag, PostLink
from .forms import *
import bleach
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError
from django.contrib import messages
from django.core.files.storage import FileSystemStorage
# Create your views here.

class ArchivePage(TemplateView):
    template_name = 'home/archie.html'

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated and request.user.is_staff:
            return render(request, self.template_name, self.get_context_data())
        else:
            return redirect('accounts:login')
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
            x = Review.objects.create(user=self.request.user, book=a, date=timezone.now(), details=text_dict['review'])


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
                x= Review.objects.create(user=self.request.user, book=a, date=timezone.now(), details=text_dict['review'])

        else:
            messages.error(self.request, 'kindly fill form accurately')
            return False



class ArchDetail(BookFormMixin,TemplateView):

    template_name = 'home/archdetail.html'

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated and request.user.is_staff:
            return render(request, self.template_name, self.get_context_data())
        else:
            return redirect('accounts:login')
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
                self.save_book_form()
            if self.request.POST.get('bookformbtn'):
                self.edit_book_form()
            return redirect('archives:archdetail')
        else:
            return redirect('accounts:login')




class Test(TemplateView):
    template_name = 'home/test.html'

    def post(self, *args, **kwargs):
        x = Book.objects.get(name= 'a')



        return redirect('archives:test')

def delete_book_view(request, pk):
    if pk and request.user.is_authenticated and request.user.is_admin:
        try:
            x = Book.objects.get(pk=pk)
            if x.user == request.user:
                x.delete()
            else:
                messages.error(request, 'not a valid user')

            return redirect('home:home')
        except:
            messages.error(request, 'Book doesnot exist')
            return redirect('home:home')

def delete_review_view(request, pk):
    if pk and request.user.is_authenticated and request.user.is_admin:
        try:
            x = Review.objects.get(pk=pk)
            if x.user == request.user:
                x.delete()
            else:
                messages.error(request, 'not a valid user')

            return redirect('home:home')
        except:
            messages.error(request, 'Book doesnot exist')
            return redirect('home:home')