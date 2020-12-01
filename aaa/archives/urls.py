from django.urls import path
from . import views

app_name = 'archives'


urlpatterns = [
    path('', views.ArchivePage.as_view(), name = 'home_archives'),
    path('details', views.ArchDetail.as_view(), name = 'archdetail'),
    path('testing', views.Test.as_view(), name='test'),
    path('del/<int:pk>', views.delete_book_view, name='deletebook'),
    path('delreview/<int:pk>', views.delete_review_view, name='deletereview')
]