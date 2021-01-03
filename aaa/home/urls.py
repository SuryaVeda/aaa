from django.urls import path
from . import views
from .models import Tag


app_name = 'home'

urlpatterns = [
path('posts/<int:pk>', views.PostDetail.as_view(), name = 'postdetail'),
path('getnewposts/<int:pk>', views.GetPosts.as_view(), name = 'getposts'),
path('', views.HomeView.as_view(), name = 'home'),
path('refreshhome', views.refresh_home_page, name = 'refresh'),
path('managewebsite', views.Manage.as_view(), name='manage'),
path('errors', views.StaffError.as_view(), name = 'stafferror'),
path('conferences', views.show_conferences, name = 'conf'),
path('searchPage', views.SearchView.as_view(), name = 'search'),
path('editdetails/<int:pk>/<int:detail_pk>', views.PostView.as_view(), name='edittagdetail'),
path('adddetails/<int:pk>', views.PostView.as_view(), name='addtagdetail'),
path('deletetag/<int:pk>/<int:detail_pk>', views.delete_tagdetail_view, name = 'deletetagdetail'),
path('delete_post/<int:pk>', views.delete_post_view, name = 'deletepost'),
path('delete_comment/<int:pk>', views.delete_comment_view, name = 'deletecomment'),
path('commentForm/<int:pk>', views.PostView.as_view(), name = 'commentform'),
path('postform', views.PostView.as_view(), name = 'postview'),
path('create_post', views.create_post_view, name='postForm'),
path('home/<str:speciality_type>', views.speciality_view, name = 'speciality')
]
