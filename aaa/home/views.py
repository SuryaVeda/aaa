from django.shortcuts import render, redirect
from .models import Post,Comment, Tag, PostLink
from archives.models import Book
from accounts.models import User
from home.mixins import ValidateLinkMixin, ValidateTextMixin, ValidateFileMixin
from .forms import CreatePostForm
from .decorators import staff_required
from django.utils import timezone
from django.contrib import messages
from django.views.generic import TemplateView
import bleach
from django.core.files.storage import FileSystemStorage

# Create your views here.
def home_view(request):
    template_name = 'home/home.html'
    posts = Post.objects.order_by('pk')
    users = User.objects.all()
    tag_speciality = Tag.objects.filter(is_speciality = True)
    context = {'posts':posts, 'users':users, 'tag_speciality':tag_speciality}
    return render(request, template_name, context)



def speciality_view(request, speciality_type):
    template_name = 'home/speciality_tag.html'
    tag = Tag.objects.get(name=speciality_type)
    subjects =list(Tag.objects.filter(is_degree = True, is_speciality = False))+ list(Tag.objects.filter(is_speciality = True))

    posts = Post.objects.filter(tag=tag).order_by('pk')
    tag_speciality = Tag.objects.filter(is_degree=True)
    context = {'tag':tag, 'tag_speciality':tag_speciality, 'posts':posts, 'subjects':subjects}
    return render(request, template_name, context)


class SearchView(TemplateView):
    template_name = 'home/search.html'
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
        context['books'] = self.get_books()
        context['tag_speciality'] = Tag.objects.filter(is_speciality=True)
        return context



def delete_post_view(request,pk):
    if pk and request.user.is_authenticated:
        try:
            x = Post.objects.get(pk = pk)
            if x.user == request.user:
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
            if x.user == request.user:
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

def create_post_view(request):
    template_name = 'home/home_post.html'
    form = CreatePostForm()
    tag_speciality = Tag.objects.filter(is_degree=True)
    context = {'form': form, 'tag_speciality': tag_speciality}
    return render(request, template_name, context)

class PostView(ValidateLinkMixin, ValidateFileMixin, ValidateTextMixin, TemplateView):
    template_name = 'home/home.html'
    def post(self, *args, **kwargs):
        print(self.request.POST)
        if self.request.POST.get('createcomment'):
            if kwargs['pk']:
                print(kwargs['pk'])
                self.save_comment(kwargs['pk'])
        if self.request.POST.get('homepostform'):
            self.save_homepost()


        return redirect('home:home')

    def save_homepost(self):
        link_dict = self.clean_links()
        template_name = 'home/home_post.html'
        form = CreatePostForm()
        form = CreatePostForm(self.request.POST, self.request.FILES)
        if form.is_valid():
            if self.request.user.is_staff or self.request.user.is_admin:
                form.save(commit=False)
                form.user = self.request.user
                form.date = timezone.now()

                a = form.save(commit=True)

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
            x = Comment.objects.create(user=self.request.user, date=timezone.now())
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
