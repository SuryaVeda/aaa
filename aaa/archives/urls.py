from django.urls import path
from . import views

app_name = 'archives'


urlpatterns = [
    path('', views.ArchivePage.as_view(), name = 'home_archives'),
    path('lecturepost/<int:pk>', views.LecturePostDetailView.as_view(), name = 'lecture_detail'),
    path('conferencepost/<int:pk>', views.ConferencePostDetailView.as_view(), name = 'conference_detail'),
    path('exfactor', views.LecturePage.as_view(), name = 'lectures'),
    path('lectures', views.LecturePage.as_view(), name = 'lectures'),
    path('send-mail/<int:pk>', views.send_mail_view, name = 'sendmail'),
    path('deletepost-detail/<int:pk>', views.delete_post_detail, name = 'deletepostdetail'),
    path('edit-lecture-detail/<int:pk>/<int:opk>', views.ProfileDetailUpdateView.as_view(), name = 'editdetails'),
    path('edit-lecture-detail/<int:opk>', views.ProfileDetailCreateView.as_view(), name = 'adddetail'),
    path('edit-lecture/<int:pk>', views.LecturePostUpdateView.as_view(), name = 'updatelecture'),
    path('delete-link/<int:pk>', views.PostLinkDeleteView.as_view(), name = 'deletelink'),
    path('edit-links/<int:pk>/<int:opk>', views.PostLinkUpdateView.as_view(), name = 'editlinks'),
    path('create-lecture', views.LecturePostCreateView.as_view(), name = 'createlecture'),
    path('create-conference', views.LecturePostCreateView.as_view(),kwargs={'conference':True}, name = 'createconference'),
    path('details', views.ArchDetail.as_view(), name = 'archdetail'),
    path('testing', views.Test.as_view(), name='test'),
    path('del/<int:pk>', views.delete_book_view, name='deletebook'),
    path('delreview/<int:pk>', views.delete_review_view, name='deletereview')
]
