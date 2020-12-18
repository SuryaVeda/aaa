from django.shortcuts import render, redirect, reverse
from django.views.generic import CreateView
from .models import Post
# Create your views here.
from .forms import *


class PostCreateView(CreateView):
    form_class = CreatePostForm
    model = Post

