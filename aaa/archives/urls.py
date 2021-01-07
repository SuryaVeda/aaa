from django.urls import path
from . import views

app_name = 'archives'


urlpatterns = [
    path('', views.ArchivePage.as_view(), name = 'home_archives'),
    path('lectures', views.LecturePage.as_view(), name = 'lectures'),
    path('deletepost-detail/<int:pk>', views.delete_post_detail, name = 'deletepostdetail'),
    path('edit-lecture-detail/<int:pk>/<int:opk>', views.ProfileDetailUpdateView.as_view(), name = 'editdetails'),
    path('edit-lecture-detail/<int:opk>', views.ProfileDetailCreateView.as_view(), name = 'adddetail'),
    path('edit-lecture/<int:pk>', views.LecturePostUpdateView.as_view(), name = 'updatelecture'),
    path('delete-link/<int:pk>', views.PostLinkDeleteView.as_view(), name = 'deletelink'),
    path('edit-links/<int:pk>/<int:opk>', views.PostLinkUpdateView.as_view(), name = 'editlinks'),
    path('create-lecture', views.LecturePostCreateView.as_view(), name = 'createlecture'),
    path('details', views.ArchDetail.as_view(), name = 'archdetail'),
    path('testing', views.Test.as_view(), name='test'),
    path('del/<int:pk>', views.delete_book_view, name='deletebook'),
    path('delreview/<int:pk>', views.delete_review_view, name='deletereview')
]
