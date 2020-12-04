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
    user = {}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.regular = 'False'
        self.google = 'False'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['google'] = self.google
        context['regular'] = self.regular
        if self.google =='False' and self.regular=='False':
            context['form'] = StaffRegisterForm()

        return context
    def get(self, request, *args, **kwargs):
        jsonobj = self.request.GET.get('google_success')
        if jsonobj:
            self.regular = 'True'
            self.google = 'True'
            SignupView.user = json.loads(jsonobj)
            print(SignupView.user)

            return render(request, self.template_name, self.get_context_data())
        else:
            self.request= 'False'
            self.google = 'False'
            return render(request, self.template_name, self.get_context_data())

    def post(self,*args,**kwargs):
        if self.request.POST.get('profile'):
            a = self.validate_google_login()
            x = redirect('accounts:staff')
            url = x.url + '?google_success=' + json.dumps(a)
            return JsonResponse(status=x.status_code, data={'success': url})

        if self.request.POST.get('signupbutton'):
            self.validate_native_signup()
            self.regular = 'True'
            self.google = 'False'
            print('google signup successfull')
            return render(self.request, self.template_name, self.get_context_data())
        if self.request.POST.get('profileformbtn'):
            print(self.request.POST)
            print(SignupView.user)
            try:
                password = self.request.POST.get('password')
                if password:
                    SignupView.user['password'] = password
            except:
                pass
            try:
                degreelist = self.save_degree_form()
                if not degreelist:
                    return redirect('accounts:staff')
                SignupView.user['degree'] = degreelist
            except:
                messages.error(self.request, 'unable to save qualifications')
                return redirect('accounts:staff')

            try:
                workobj = self.save_work_form()
                if workobj:
                    SignupView.user['work'] = workobj

            except:
                pass
            usr = User.objects.create_staff(SignupView.user['email'], SignupView.user['username'], SignupView.user['password'])
            usr.staff = False
            usr.username = SignupView.user['username']
            usr.save()
            profile = usr.save_profile
            for i in SignupView.user['degree']:
                profile.degree.add(i)
            profile.work.add(SignupView.user['work'])
            profile.save()
            return redirect('accounts:login')


    def validate_google_login(self):
        try:
            profile = self.request.POST.get('profile')
            j = json.loads(profile)
            name = j["name"]
            email = j["email"]
            print(name)
            print(email)
            if name and email:
                try:
                    User.objects.get(email=email)
                    messages.error(self.request, 'user with above email already exists!!, Kindly go to log in page')
                    x= redirect('accounts:login')
                    return JsonResponse(status=x.status_code, data={'success': x.url})
                except:
                    self.user['username'] = name
                    self.user['email'] = email
                    return self.user
            else:
                x = redirect('accounts:staff')
                print(x)
                return JsonResponse(status=x.status_code, data={'success': x.url})


        except:
            messages.error(self.request, 'Unable to validate your google details. Kindly signup from the website.')
            x = redirect('accounts:staff')
            return JsonResponse(status=x.status_code, data={'success': x.url})

    def validate_native_signup(self):
        validate_email = EmailValidator()
        email = self.request.POST.get('email')
        password = self.request.POST.get('password')
        username = self.request.POST.get('username')
        try:
            validate_email(email)
            try:
                User.objects.get(email = email)
                messages.error(self.request, 'user with above email already exists!!, Kindly go to log in page')
                return redirect('accounts:staff')
            except:
                self.user['email'] = email

        except:
            messages.error(self.request, 'Enter Valid email')
            return redirect('accounts:staff')
        if username and password:
            self.user['username']=bleach.clean(username, strip=True)
            self.user['password']= password
        else:
            messages.error(self.request, 'Enter Username and password correctly')
            return redirect('accounts:staff')
        return self.user

class MyProfile(DetailFormMixin, WorkFormMixin, DegreeFormMixin,PersonalFormMixin, ContactFormMixin, TemplateView):
    template_name = 'accounts/profile.html'
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated and request.user.is_staff:
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

