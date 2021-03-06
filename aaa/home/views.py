from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models import Post,Comment, Tag, PostLink
from notifications.mixins import CreateNotificationMixin
from archives.models import Book, LecturePost
from django.utils.decorators import method_decorator
from accounts.models import User, ProfileDetail
from home.mixins import ValidateLinkMixin, ValidateTextMixin, ValidateFileMixin, GeneralContextMixin
from .forms import CreatePostForm
from .decorators import staff_required, admin_required
from django.utils import timezone
from django.contrib import messages
from django.views.generic import TemplateView
import bleach, datetime,pytz
from django.core.files.storage import FileSystemStorage
from django.conf import settings
from  django.core.mail import send_mail
from django.core.exceptions import ObjectDoesNotExist
from django.views import View
from mcq.models import QuestionBank
from notifications.models import Notification, Message
from archives.models import LecturePost
from fb.mixins import PublishInFacebook
# Create your views here.
class Manage(TemplateView):
    template_name = 'home/manage.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data( **kwargs)
        if self.request.user.is_staff:
            context['users'] = User.objects.order_by('-pk')
            context['users_length'] = len(context['users'])
            tag_speciality = Tag.objects.filter(is_speciality=True)
            context['tag_speciality'] = list(tag_speciality)

        return context
def email(request):
    subject = 'You visited conference page'
    message = ' it  means a world to us '
    email_from = settings.EMAIL_HOST_USER
    recipient_list = ['suryaveda@hotmail.com',]
    send_mail( subject, message, email_from, recipient_list )
    return redirect('home:home')

class HomeView(PublishInFacebook,TemplateView):
    template_name = 'home/home.html'
    posts = []
    postslist = []

    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)
        questionbank = QuestionBank.objects.all()
        context['questionbank'] = list(questionbank.filter(mcq=True))
        context['flashcards'] = list(questionbank.filter(flashcard=True))
        postslist = list(Post.objects.filter(lecture=False, conference=False).order_by('-date').prefetch_related())


        print(len(postslist))
        utc = pytz.UTC
        tz = pytz.timezone('Asia/Kolkata')
        today = datetime.datetime.now(tz)
        context['lectures'] = [i for i in LecturePost.objects.filter(lecture=True).order_by('-pk') if utc.localize(i.lecture_start_date) > today]
        context['conferences'] = [i for i in LecturePost.objects.filter(lecture=False).order_by('lecture_start_date') if utc.localize(i.lecture_start_date) > today]
        context['posts'] = postslist[0:15]

        tag_speciality = Tag.objects.filter(is_speciality=True)
        context['tag_speciality'] = list(tag_speciality)
        return context

def refresh_home_page(request):
    HomeView.tag_speciality  = Tag.objects.filter(is_speciality=True)
    print(HomeView.posts)
    HomeView.postslist.clear()
    HomeView.postslist = list(Post.objects.order_by('-date').prefetch_related())
    return redirect('home:home')


class StaffError(TemplateView):
    template_name = 'home/stafferror.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['tag_speciality'] = Tag.objects.filter(is_speciality=True)
        return context


def show_conferences(request):
    a= Tag.objects.get(name = 'Conferences')
    posts = a.post_set.all().order_by('-pk')
    tag_speciality = Tag.objects.filter(is_speciality=True)
    return render(request, 'home/conference.html', {'posts':posts,'tag_speciality': tag_speciality})

def speciality_view(request, speciality_type):

    if request.user:
        template_name = 'home/speciality_tag.html'
        context = {}
        try:
            tag = Tag.objects.get(name=speciality_type)

            if speciality_type=='NEET-SS':
                questionbank = QuestionBank.objects.all()
                template_name = 'home/neet.html'
                context['questionbank'] = list(questionbank.filter(mcq=True))
                context['flashcards'] = list(questionbank.filter(flashcard=True))
                context['cases'] = list(questionbank.filter(qa=True))


            subjects = list(Tag.objects.filter(is_degree=True))

            posts = Post.objects.filter(tag=tag, lecture=False).order_by('-pk')
            tag_speciality = Tag.objects.filter(is_speciality=True)
            context['tag'] = tag
            context['tag_speciality'] = tag_speciality
            context['posts'] = posts
            context['subjects'] = subjects
            return render(request, template_name, context)
        except:
            messages.error(request, 'unable to fetch the page.')
            return redirect('home:home')

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
        posts = Post.objects.filter(heading__icontains = query, lecture=False)
        return list(posts)

    def get_books(self):
        searchInput = self.request.GET.get('searchinput')
        if not searchInput:
            messages.error(self.request, 'Enter something in search!')
            return False
        query = bleach.clean(searchInput, strip=True)
        books = Book.objects.filter(name__icontains=query)
        return list(books)
    def get_lectures(self):
        searchInput = self.request.GET.get('searchinput')
        if not searchInput:
            messages.error(self.request, 'Enter something in search!')
            return False
        query = bleach.clean(searchInput, strip=True)
        books = LecturePost.objects.filter(heading__icontains=query)
        return list(books)

    def get_context_data(self, **kwargs):
        context = super(SearchView, self).get_context_data(**kwargs)
        context['tag_speciality'] = Tag.objects.filter(is_speciality=True)
        searchInput = self.request.GET.get('searchinput')
        if not searchInput:
            context['someresults'] = True
            return context
        context['posts'] = self.get_posts()

        context['lectures'] = self.get_lectures()
        if self.request.user.is_staff:
            context['books'] = self.get_books()
        else:
            context['books'] = False

        if context['posts'] and context['books'] and context['lectures']:
            context['someresults'] = True
        else:
            context['someresults'] = False
        return context



def delete_post_view(request,pk):
    ex= redirect('home:home')
    if pk and request.user.is_authenticated:

        try:
            x = Post.objects.get(pk = pk)
            if x.user == request.user or request.user.is_admin:
                print(x.get_absolute_url())
                Message.objects.delete_messages(x.get_absolute_url())
                x.delete()
                ex = refresh_home_page(request)
                print(ex.url)
                print(ex.status_code)
                return JsonResponse({'success': ex.url}, safe=False)
            else:
                messages.error(request, 'not a valid user')
                return JsonResponse({'success': ex.url}, safe=False)


        except:
            messages.error(request, 'post is not present in database')
            return JsonResponse({'success': ex.url}, safe=False)
    else:
        messages.error(request, 'select valid post')

        return JsonResponse({'success': ex.url}, safe=False)


def delete_comment_view(request,pk):
    ex= redirect('home:home')
    if pk and request.user.is_authenticated:
        try:
            x = Comment.objects.get(pk = pk)
            if x.user == request.user or request.user.is_admin:
                x.delete()
                ex = refresh_home_page(request)
                print(ex.url)
                return JsonResponse({'success': ex.url}, safe=False)
            else:
                messages.error(request, 'not a valid user')
                return JsonResponse({'success': ex.url}, safe=False)
        except:
            messages.error(request, 'post is not present in database')
            return JsonResponse({'success': ex.url}, safe=False)
    else:
        messages.error(request, 'select valid post')

        return JsonResponse({'success': ex.url}, safe=False)


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

            return redirect('/home/{0}'.format(y.name))
        except:
            print('some problem')
            messages.error(request, 'post is not present in database')
            return redirect('home:home')
    else:
        messages.error(request, 'select valid post')

        return redirect('home:home')
@staff_required
def create_post_view(request):
    if request.user and request.user:
        print('hello')
        template_name = 'home/home_post.html'
        form = CreatePostForm()

        tags = Tag.objects.all()
        tag_speciality = tags.filter(is_speciality=True)
        context = {'form': form, 'tag_speciality': tag_speciality, 'tags':tags}
        return render(request, template_name, context)
    else:
        return redirect('accounts:login')

@method_decorator(staff_required, name = 'dispatch')
class PostView(PublishInFacebook,CreateNotificationMixin,ValidateLinkMixin, ValidateFileMixin, ValidateTextMixin, TemplateView):
    template_name = 'home/home.html'
    def get_user(self):
        if self.request.user.is_staff:
            return self.request.user
        else:
            return None
    def post(self, *args, **kwargs):
        if self.request.user and self.request.user:
            print(self.request.POST)
            if self.request.POST.get('createcomment'):
                if kwargs['pk']:
                    print(kwargs['pk'])
                    self.save_comment(kwargs['pk'])
                    return redirect('home:refresh')
            if self.request.POST.get('homepostform'):
                result = self.save_homepost()
                if not result:
                    return redirect('home:postForm')
                return redirect('home:refresh')
            if self.request.POST.get('addtagdetail'):
                self.save_tagdetail(kwargs['pk'])
                try:
                    x = Tag.objects.get(pk=int(kwargs['pk']))
                    return redirect('/home/{0}'.format(x.name))
                except:
                    return redirect('home:home')

            if self.request.POST.get('edittagdetail'):
                print(kwargs['detail_pk'])
                self.edit_tagdetail(kwargs['pk'], kwargs['detail_pk'])

                try:
                    x = Tag.objects.get(pk=int(kwargs['pk']))
                    return redirect('/home/{0}'.format(x.name))
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
        print(self.request.POST)
        if not self.request.POST.get('tag'):
            messages.error(self.request, 'Add a Tag/Subject.', extra_tags = self.request.user.email)
            return False

        if form.is_valid():
            if self.request.user or self.request.user:
                form.save(commit=False)
                if self.request.user.is_staff:
                    form.user = self.request.user

                a = form.save(commit=True)
                a.user = self.request.user
                a.save()
                post = a
                if post.user.is_staff:
                    mess = Message.objects.create(post_url = post.get_absolute_url(), type = 'post', text = 'A new post is added  {0}.. by user {1}'.format(post.heading[:10], post.user.username))
                    mess.create_notifications(post.user)

                if link_dict:
                    if link_dict['links']:
                        for i in link_dict['links']:
                            linkobj = PostLink.objects.create(user=self.get_user(), link=i[1], link_name=i[0])
                            a.link.add(linkobj)
                            a.save()

                if not settings.DEBUG:
                    try:
                        self.publish_facebook(a)
                    except Exception as e:
                        print('cannot publish in facebook')
                return True
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
            x = Comment.objects.create(user=self.get_user())
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
                        linkobj = PostLink.objects.create(user=self.get_user(), link=i[1], link_name=i[0])
                        x.link.add(linkobj)
            x.save()
            post.comments.add(x)
            self.create_comment_notification(post)
            post.save()

        except:
            messages.error(self.request, 'error in saving')


class GetPosts(View):
    def get_user(self):
        if self.request.user.is_staff:
            return self.request.user
        else:
            return None

    def get(self, request, *args, **kwargs):
        print('get request')
        if kwargs['pk']:
            index = kwargs['pk']
            try:
                index = int(index)
            except:
                print('enter integer')
                return redirect('home:home')
            postslist = []
            oldpostslist = list(Post.objects.filter(lecture=False, conference=False).order_by('-date').prefetch_related())

            for i in oldpostslist:
                if i.tag.filter(name = 'Conferences'):
                    continue
                else:
                    postslist.append(i)
            newposts = postslist[index:index + 15]
            html = [ (((render(self.request, 'home/getposts.html',{'user': self.get_user(), 'post': i})).content).decode('utf-8')).strip() for i in newposts]

            response =JsonResponse(html, safe=False)
            print(response.status_code)
            print(html)

            return response

        else:
            return redirect('home:home')

class PostDetail(TemplateView):
    template_name = 'home/postdetail.html'
    def get(self, request, *args, **kwargs):
        try:
            post = Post.objects.get(pk=kwargs['pk'])
            context = self.get_context_data()
            context['post'] = post
        except Exception as e:
            messages.error(self.request, 'Post is deleted.')
            return redirect('home:home')
        return render(request, self.template_name, context)


@method_decorator(staff_required, name = 'dispatch')
class YourPost(TemplateView):
    template_name = 'home/myposts.html'
    def get(self, request, *args, **kwargs):
        username = kwargs['username']
        x = User.objects.filter(username = username)
        if x:
            return super().get(request, *args, **kwargs)
        else:
            messages.error(request, 'invalid user', extra_tags = self.request.user.email)
            return redirect('home:home')
        try:

            username = kwargs['username']
            x = User.objects.filter(username = username)
            if x:
                return super().get(request, *args, **kwargs)
            else:
                messages.error(request, 'invalid user', extra_tags = self.request.user.email)
                return redirect('home:home')

        except Exception as e:
            return redirect('home:home')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        utc = pytz.UTC
        tz = pytz.timezone('Asia/Kolkata')
        today = datetime.datetime.now(tz)
        tag_speciality = Tag.objects.filter(is_speciality=True)
        context['tag_speciality'] = tag_speciality
        context['lectures'] = [i for i in LecturePost.objects.filter(lecture=True, user = self.request.user).order_by('-pk') if utc.localize(i.lecture_start_date) > today]
        context['conferences'] = [i for i in LecturePost.objects.filter(lecture=False, user = self.request.user).order_by('lecture_start_date') if utc.localize(i.lecture_start_date) > today]

        context['posts'] = Post.objects.filter(user = self.request.user)
        return context
