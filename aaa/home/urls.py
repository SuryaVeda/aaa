from django.urls import path
from . import views
from .models import Tag


app_name = 'home'

urlpatterns = [
path('', views.home_view, name = 'home'),
path('searchPage', views.SearchView.as_view(), name = 'search'),
path('delete_post/<int:pk>', views.delete_post_view, name = 'deletepost'),
path('delete_comment/<int:pk>', views.delete_comment_view, name = 'deletecomment'),
path('commentForm/<int:pk>', views.PostView.as_view(), name = 'commentform'),
path('postform', views.PostView.as_view(), name = 'postview'),
path('create_post', views.create_post_view, name='postForm'),
path('home/<str:speciality_type>', views.speciality_view, name = 'speciality')
]

