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
import json, bleach
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

# Create your views here.

def login_view(request):
    if request.user.is_authenticated:
        return redirect('home:home')
    template_name = 'accounts/login.html'
    form = LoginForm()
    tag_speciality = Tag.objects.filter(is_speciality=True)
    if request.method== 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            try:
                user = authenticate(request, email=form.cleaned_data.get('email'), password=form.cleaned_data.get('password'))
                if user is not None:
                    login(request, user)
                    return redirect('home:home')
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
        if request.user.is_authenticated:
            return redirect('home:home')
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
        if self.request.user.is_authenticated:
            return redirect('home:home')

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
            try:
                degreelist = self.save_degree_form()
                if not degreelist:
                    return render(self.request, 'accounts/commonsignup.html',
                                  {'email': email, 'username': username})
                user['degree'] = degreelist
            except:
                messages.error(self.request, 'unable to save qualifications')
                return render(self.request, 'accounts/commonsignup.html', {'email': email, 'username': username})

            try:
                workobj = self.save_work_form()
                if workobj:
                    user['work'] = workobj
                else:
                    user['work'] = ''

            except:
                user['work'] = ''
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
                return redirect('accounts:login')
            else:
                messages.error(self.request, 'Invalid user details')
                return redirect('accounts:staff')


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
            return redirect('accounts:login')

