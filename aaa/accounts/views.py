from django.shortcuts import render, redirect, get_object_or_404
from .forms import *
from .models import Profile,User,ProfileDetail, Work, Degree, MedicalCollege
from home.models import Tag, ImageAdd, PostLink
from home.mixins import *
from home.decorators import staff_required
from datetime import date, timedelta
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from urllib.parse import parse_qs
import json, bleach, string, random
from django.contrib import messages
from .forms import LoginForm
from django.contrib.auth import authenticate, login
from django.views import View
from django.views.generic import TemplateView
from django.core.validators import URLValidator, EmailValidator
from django.core.exceptions import ValidationError
from django.http import JsonResponse
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.conf import settings
from django.core.mail import send_mail

# Create your views here.

''''''




def login_view(request):

    template_name = 'accounts/login.html'
    form = LoginForm()
    tag_speciality = Tag.objects.filter(is_speciality=True)
    if request.method== 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            try:
                print(request.POST.get('email'))
                print(request.POST.get('password'))
                user = authenticate(request, email=request.POST.get('email'),
                                    password=request.POST.get('password'))
                if user is not None:
                    login(request, user)
                    return redirect('archives:lectures')
                else:
                    messages.error(request, "Credentials are either wrong or not registered.")
                    print('see try statemetn')
                    return redirect('accounts:login')


            except:
                print('see except statement')
                messages.error(request, "Credentials are either wrong or not registered.")
                return redirect('accounts:login')

        else:
            messages.error(request, 'invalid form, kindly enter email id')

            return redirect('accounts:login')

    return render(request, template_name, {'form':form, 'tag_speciality':tag_speciality})


def password_reset_view(request):
    pass

def user_signout(request):
    user = request.user
    logout(request)
    return redirect('home:home')


class PasswordReset(TemplateView):
    template_name = 'accounts/password_reset.html'
    def encrypt(self):
        obj = settings.SECRET_KEY.ljust(16)[:16]
        y= string.ascii_letters
        for i in range(10):
            obj += random.choice(y)
        return obj


    def get(self, request, *args, **kwargs):
        if request.GET.get('emailform'):
            return render(request, PasswordReset.template_name, self.get_context_data())
        if request.GET.get('emailsent'):
            return render(request, PasswordReset.template_name,{'email_sent':True})
        if request.GET.get('passwordreset'):
            code = request.GET.get('passwordreset')
            print(code)
            try:
                x = User.objects.get(reset = request.GET.get('passwordreset'))
                print(x.reset)

                return render(request, PasswordReset.template_name, {'resetpassword':True, 'code':code})


            except Exception as e:
                return redirect('accounts:login')
        return redirect('accounts:login')


    def post(self, *args, **kwargs):
        print(self.request.POST)
        if self.request.POST.get('passform'):
            code = self.request.POST.get('code')
            user = User.objects.get(reset = code)
            try:
                user = User.objects.get(reset = code)
                user.set_password(self.request.POST.get('password'))
                user.reset = None
                print(user.password)
                user.save()
                print(user.password)
                return redirect('accounts:login')
            except Exception as e:
                print('error in saving')
                messages.error(self.request,'Invalid reset link, create a new link', extra_tags = self.request.user.email )
                return redirect('accounts:login')
        if self.request.POST.get('emailformpost'):
            try:
                print(self.request.POST)
                user = User.objects.get(email = self.request.POST.get('email'))
                obj = self.encrypt()
                user.reset = obj
                print(user.reset)
                user.save()
                send_mail("Reset password for your AAA account", "Kindly press the below link or copy and paste it in browser \n \n {0}/accounts/passreset?passwordreset={1}".format(settings.DOMAIN_NAME, obj), settings.EMAIL_HOST_USER, [user.email], fail_silently=True)
                print('email sent')
                return redirect(reverse('accounts:password_reset_form') + '?emailsent=True')

            except Exception as e:
                messages.error(self.request, 'invalid email or email doesnot exist', extra_tags=self.request.user.email)

        return redirect('accounts:login')


class SignupView(WorkFormMixin,DegreeFormMixin,ValidateTextMixin,TemplateView):
    template_name = 'accounts/commonsignup.html'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.regular = 'False'
        self.google = 'False'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = StaffRegisterForm()

        return context
    def get(self, request, *args, **kwargs):

        if request.GET.get('email') and request.GET.get('username'):
            email = request.GET.get('email')
            try:
                User.objects.get(email=email)
                messages.error(self.request, 'user with above email already exists!!, Kindly go to log in page')
                return redirect('accounts:staff')
            except:
                pass

            username = request.GET.get('username')
            context = {'email': email, 'username': username}
            return render(request, 'accounts/commonsignup.html', context)

        else:

            return render(request, 'accounts/signup.html', self.get_context_data())


    def post(self,*args,**kwargs):


        if self.request.POST.get('profileformbtn'):
            print(self.request.POST)
            user = {}
            email = self.request.POST.get('email')
            username = self.request.POST.get('username')
            password = self.request.POST.get('password')

            try:

                if email and username and password:
                    validate_email = EmailValidator()

                    try:
                        email = bleach.clean(email, strip=True)
                        validate_email(email)
                        username = bleach.clean(username, strip=True)
                        password = bleach.clean(password, strip=True)
                    except:
                        messages.error(self.request, 'Enter email, username or password correctly.')
                        return render(self.request, 'accounts/commonsignup.html',
                                      {'email': email, 'username': username})

                    user['email'] = email
                    user['username'] = username
                    user['password'] = password
                else:
                    messages.error(self.request, 'Enter username, email, password correctly.')
                    return render(self.request, 'accounts/commonsignup.html',
                                  {'email': email, 'username': username})
            except:
                messages.error(self.request, 'Enter username, email, password correctly.')
                return render(self.request, 'accounts/commonsignup.html', {'email': email, 'username': username})
            print('reached 1')
            degreelist = self.save_degree_form()
            if not degreelist:
                return render(self.request, 'accounts/commonsignup.html',
                              {'email': email, 'username': username})
            user['degree'] = degreelist
            print(user)
            try:
                degreelist = self.save_degree_form()
                if not degreelist:
                    return render(self.request, 'accounts/commonsignup.html',
                                  {'email': email, 'username': username})
                user['degree'] = degreelist
                print(user)
            except:
                messages.error(self.request, 'unable to save qualifications')
                return render(self.request, 'accounts/commonsignup.html', {'email': email, 'username': username})
            print('reached 2')
            try:
                workobj = self.save_work_form()
                if workobj:
                    user['work'] = workobj
                else:
                    user['work'] = ''

            except:
                user['work'] = ''
            print('reached 3')
            if user['email'] and user['password'] and user['username']:
                usr = User.objects.create_staff(user['email'], user['username'],
                                                user['password'])
                usr.staff = False
                usr.username = user['username']
                usr.save()
                profile = usr.save_profile
                for i in user['degree']:
                    if i:
                        profile.degree.add(i)
                if user['work']:
                    profile.work.add(user['work'])

                profile.save()
                print('reached 4')
                return redirect('accounts:login')
            else:
                messages.error(self.request, 'Invalid user details')
                return redirect('accounts:staff')

class ChangeUser(View):
    def get(self, request, *args, **kwargs):
        if request.user.is_admin and request.user.email == 'vijay.adabala96@gmail.com' or request.user.email == 'suryaveda@hotmail.com':
            return redirect('home:manage')
        else:
            return redirect('home:home')

    def post(self, *args, **kwargs):
        if self.request.user.is_admin and self.request.user.email == 'vijay.adabala96@gmail.com' or self.request.user.email == 'suryaveda@hotmail.com':
            if self.request.POST.get('promoteadmin'):
                try:
                    x = User.objects.get(pk = kwargs.get('pk'))
                    x.admin = True
                    x.staff = True
                    x.save()
                    print(x.is_admin)
                except:
                    messages.error(self.request, 'User doesnot exist', extra_tags='{0}'.format(self.request.user.email))
                    return redirect('home:manage')
            if self.request.POST.get('promotestaff'):
                try:
                    x = User.objects.get(pk=kwargs.get('pk'))
                    x.staff = True
                    x.admin = False
                    x.save()
                    print(x.is_staff)
                except:
                    messages.error(self.request, 'User doesnot exist', extra_tags='{0}'.format(self.request.user.email))
                    return redirect('home:manage')
            if self.request.POST.get('demotestaff'):
                try:
                    x = User.objects.get(pk=kwargs.get('pk'))
                    x.admin = False
                    x.staff = True
                    x.save()
                    print(x.is_admin)
                except:
                    messages.error(self.request, 'User doesnot exist', extra_tags='{0}'.format(self.request.user.email))
                    return redirect('home:manage')
            if self.request.POST.get('deleteuser'):
                try:
                    x = User.objects.get(pk=kwargs.get('pk'))
                    x.delete()
                except:
                    messages.error(self.request, 'User doesnot exist', extra_tags='{0}'.format(self.request.user.email))
                    return redirect('home:manage')
            x = redirect('home:manage')
            return JsonResponse({'success':x.url}, safe=False)
        else:
            return redirect('home:home')

class MyProfile(DetailFormMixin, WorkFormMixin, DegreeFormMixin,PersonalFormMixin, ContactFormMixin, TemplateView):
    template_name = 'accounts/profile.html'
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated :
            return render(request, self.template_name, self.get_context_data())
        else:
            return redirect('accounts:login')
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['profile'] = Profile.objects.get(user=self.request.user)
        context['tag_speciality'] = Tag.objects.filter(is_degree = True)

        context['degree_tags']=Tag.objects.filter(is_degree=True)
        return context

    def post(self, *args, **kwargs):
        if self.request.user.is_authenticated and self.request.user.is_staff:
            if self.request.method == 'POST':
                print(self.request.POST)
                self.myprofile= Profile.objects.get(user=self.request.user)
                if self.request.POST.get('contact_form_button'):
                    self.save_contact_form()
                    return redirect('accounts:myprofile')
                if self.request.POST.get('personalformbtn'):
                    self.save_personal_form()
                    return redirect('accounts:myprofile')

                if self.request.POST.get('degreeformbtn'):
                    self.save_degree_form()
                    return redirect('accounts:myprofile')
                if self.request.POST.get('workformbtn'):
                    self.save_work_form()
                    return redirect('accounts:myprofile')
                if self.request.POST.get('profdetailsform'):
                    a = self.save_detail_prof_form()
                    return redirect('accounts:myprofile')

            else:
                print('not a post request')
                return redirect('accounts:myprofile')
        else:
            pass
