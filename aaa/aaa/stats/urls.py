from django.urls import path
from . import views

app_name = 'stats'

urlpatterns = [
path('', views.StatPage.as_view(), name = 'stat')
]
