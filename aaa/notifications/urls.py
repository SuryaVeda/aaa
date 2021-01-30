from django.urls import path
from . import views

app_name = 'notifications'

urlpatterns = [
path('', views.ShowNotification.as_view(), name = 'base'),

]
