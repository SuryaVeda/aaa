from django.shortcuts import render, redirect
from .models import Post,Comment, Tag, PostLink
from archives.models import Book
from accounts.models import User, ProfileDetail
from home.mixins import ValidateLinkMixin, ValidateTextMixin, ValidateFileMixin
from .forms import CreatePostForm
from .decorators import staff_required
from django.utils import timezone
from django.contrib import messages
from django.views.generic import TemplateView
import bleach, datetime
from django.core.files.storage import FileSystemStorage
from django.conf import settings
from  django.core.mail import send_mail
# Create your views here.

class Manage(TemplateView):
    template_name = 'home/manage.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data( **kwargs)
        context['users'] = User.objects.all()
def email(request):
    subject = 'You visited conference page'
    message = ' it  means a world to us '
    email_from = settings.EMAIL_HOST_USER
    recipient_list = ['suryaveda@hotmail.com',]
    send_mail( subject, message, email_from, recipient_list )
    return redirect('home:home')
def home_view(request):
    if request.user:
        template_name = 'home/home.html'
        posts = Post.objects.order_by('date').reverse()
        tag_speciality = Tag.objects.filter(is_speciality=True)
        context = {'posts': posts,  'tag_speciality': tag_speciality}
        return render(request, template_name, context)
    else:
        return redirect('accounts:login')


class StaffError(TemplateView):
    template_name = 'home/stafferror.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['tag_speciality'] = Tag.objects.filter(is_speciality=True)
        return context


def show_conferences(request):
    a= Tag.objects.get(name = 'Conferences')
    posts = a.post_set.all().order_by('pk')
    return render(request, 'home/conference.html', {'posts':posts})

def speciality_view(request, speciality_type):
    if request.user:
        template_name = 'home/speciality_tag.html'
        tag = Tag.objects.get(name=speciality_type)
        subjects = list(Tag.objects.filter(is_degree=True, is_speciality=False)) + list(
            Tag.objects.filter(is_speciality=True))

        posts = Post.objects.filter(tag=tag).order_by('pk')
        tag_speciality = Tag.objects.filter(is_speciality=True)
        context = {'tag': tag, 'tag_speciality': tag_speciality, 'posts': posts, 'subjects': subjects}
        return render(request, template_name, context)
    else:
        return redirect('accounts:login')



class SearchView(TemplateView):

    template_name = 'home/search.html'

    def get(self, request, *args, **kwargs):
        if request.user:
            return render(request, self.template_name, self.get_context_data())
        else:
            return redirect('accounts:login')
    def get_posts(self):
        searchInput = self.request.GET.get('searchinput')
        if not searchInput:
            messages.error(self.request, 'Enter something in search!')
            return False
        query = bleach.clean(searchInput, strip=True)
        posts = Post.objects.filter(heading__icontains = query)
        return list(posts)

    def get_books(self):
        searchInput = self.request.GET.get('searchinput')
        if not searchInput:
            messages.error(self.request, 'Enter something in search!')
            return False
        query = bleach.clean(searchInput, strip=True)
        books = Book.objects.filter(name__icontains=query)
        return list(books)

    def get_context_data(self, **kwargs):
        context = super(SearchView, self).get_context_data(**kwargs)
        context['posts'] = self.get_posts()
        if self.request.user.is_staff:
            context['books'] = self.get_books()
        else:
            context['books'] = False

        context['tag_speciality'] = Tag.objects.filter(is_speciality=True)
        return context



def delete_post_view(request,pk):
    if pk and request.user.is_authenticated:
        try:
            x = Post.objects.get(pk = pk)
            if x.user == request.user or request.user.is_admin:
                x.delete()
            else:
                messages.error(request, 'not a valid user')
            return redirect('home:home')
        except:
            messages.error(request, 'post is not present in database')
            return redirect('home:home')
    else:
        messages.error(request, 'select valid post')

        return redirect('home:home')
def delete_comment_view(request,pk):
    if pk and request.user.is_authenticated:
        try:
            x = Comment.objects.get(pk = pk)
            if x.user == request.user or request.user.is_admin:
                x.delete()
            else:
                messages.error(request, 'not a valid user')
            return redirect('home:home')
        except:
            messages.error(request, 'post is not present in database')
            return redirect('home:home')
    else:
        messages.error(request, 'select valid post')

        return redirect('home:home')
def delete_tagdetail_view(request,pk,detail_pk):
    if pk and request.user.is_authenticated and request.user.is_admin:
        try:
            print(type(pk))
            y = Tag.objects.get(pk = pk)
            x = y.get_details
            print(x)
            for i in x:
                if i.pk == detail_pk :
                    print(i)
                    i.delete()
                else:
                    messages.error(request, 'not a valid user')

            return redirect('home:home')
        except:
            print('some problem')
            messages.error(request, 'post is not present in database')
            return redirect('home:home')
    else:
        messages.error(request, 'select valid post')

        return redirect('home:home')

def create_post_view(request):
    if request.user.is_authenticated and request.user.is_staff:
        template_name = 'home/home_post.html'
        form = CreatePostForm()
        tag_speciality = Tag.objects.filter(is_degree=True)
        context = {'form': form, 'tag_speciality': tag_speciality}
        return render(request, template_name, context)
    else:
        return redirect('accounts:login')


class PostView(ValidateLinkMixin, ValidateFileMixin, ValidateTextMixin, TemplateView):
    template_name = 'home/home.html'

    def post(self, *args, **kwargs):
        if self.request.user.is_staff and self.request.user.is_authenticated:
            print(self.request.POST)
            if self.request.POST.get('createcomment'):
                if kwargs['pk']:
                    print(kwargs['pk'])
                    self.save_comment(kwargs['pk'])
            if self.request.POST.get('homepostform'):
                self.save_homepost()
            if self.request.POST.get('addtagdetail'):
                self.save_tagdetail(kwargs['pk'])
                try:
                    x = Tag.objects.get(pk=int(kwargs['pk']))
                    return redirect('speciality', args = (x.name,))
                except:
                    return redirect('home:home')

            if self.request.POST.get('edittagdetail'):
                print(kwargs['detail_pk'])
                self.edit_tagdetail(kwargs['pk'], kwargs['detail_pk'])

                try:
                    x = Tag.objects.get(pk=int(kwargs['pk']))
                    return redirect('speciality', args=(x.name,))
                except:
                    return redirect('home:home')

            return redirect('home:home')
        else:
            return redirect('accounts:login')

    def save_tagdetail(self, pk):
        print(self.request.POST)
        text_dict = self.clean_text(['heading', 'details'])
        try:
            x = Tag.objects.get(pk = int(pk))
            if x.get_details:
                for i in x.get_details:
                    if i.heading == text_dict['heading']:
                        messages.error(self.request, 'Subject details with above heading already present. Kindly edit instead of adding new one')
                        return False
            tagdetailobj = ProfileDetail.objects.create(heading=text_dict['heading'],
                                                        details=text_dict['details'],
                                                        )
            x.details.add(tagdetailobj)
            x.save()



        except:
            print('prob in saving')
            pass





    def edit_tagdetail(self, pk, detail_pk):
        print(self.request.POST)
        print(detail_pk)
        text_dict = self.clean_text(['heading', 'details'])
        try:
            x = Tag.objects.get(pk=int(pk))
            print(x)
            if x.get_details:
                print(x.get_details)
                for i in x.get_details:
                    print(i.pk)
                    if i.pk == int(detail_pk):
                        i.heading = text_dict['heading']
                        i.details = text_dict['details']
                        i.save()
                        print('success')
                        return i
                    else:
                        messages.error(self.request,
                                       'Subject details with above heading not present')
                return False

        except:
            messages.error(self.request,
                           'Error in saving')
            return False

    def save_homepost(self):
        link_dict = self.clean_links()
        template_name = 'home/home_post.html'
        form = CreatePostForm()
        form = CreatePostForm(self.request.POST, self.request.FILES)
        if form.is_valid():
            if self.request.user.is_staff or self.request.user.is_admin:
                form.save(commit=False)
                form.user = self.request.user

                a = form.save(commit=True)
                print (a)
                print(a.user)
                a.user = self.request.user
                a.save()
                print(a.user)

                print(a.date)
                if link_dict:
                    if link_dict['links']:
                        for i in link_dict['links']:
                            linkobj = PostLink.objects.create(user=self.request.user, link=i[1], link_name=i[0])
                            a.link.add(linkobj)
                            a.save()
                return redirect('home:home')
            else:
                print('not authenticated')
                return redirect('home:postForm')
        else:
            print('not valid form')
            return redirect('home:postForm')


    def save_comment(self,pk):
        text_dict = self.clean_text(['text', 'pdf_name'])
        file_dict = self.clean_file(['image','pdf'])
        link_dict = self.clean_links()
        try:
            post = Post.objects.get(pk=pk)
            x = Comment.objects.create(user=self.request.user)
            if not text_dict['text']:
                messages.error(self.request, 'kindly enter comment text')
                return False
            x.text = text_dict['text']
            try:
                if text_dict['pdf_name'] and file_dict['pdf']:
                    storage = FileSystemStorage()
                    filename = storage.save('commentpdfs/{0}'.format(text_dict['pdf_name']), file_dict['pdf'])
                    with storage.open(filename) as f:
                        x.pdf.save(filename, f, save=True)
                    x.pdf_name = text_dict['pdf_name']

                    print('hey this is the {0}'.format(x.pdf.name))
            except:
                pass
            try:
                if file_dict['image']:
                    storage = FileSystemStorage()
                    filename = storage.save('commentimages/{0}'.format(file_dict['image'].name), file_dict['image'])
                    with storage.open(filename) as f:
                        x.img.save(filename, f, save=True)
            except:
                pass


            if link_dict:
                if link_dict['links']:
                    for i in link_dict['links']:
                        linkobj = PostLink.objects.create(user=self.request.user, link=i[1], link_name=i[0])
                        x.link.add(linkobj)
            x.save()
            post.comments.add(x)
            post.save()
        except:
            messages.error(self.request, 'error in saving')
