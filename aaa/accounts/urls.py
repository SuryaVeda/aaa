from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
path('signin', views.login_view, name = 'login' ),
path('pass_reset', views.password_reset_view, name = 'password_reset' ),
path('signup/staff_signup', views.SignupView.as_view(), name='staff' ),
path('signup/<str:email>/<str:username>', views.SignupView.as_view(), name = 'commonsignup'),
path('signout', views.user_signout, name = 'logout' ),
path('profile', views.MyProfile.as_view(), name = 'myprofile' ),
path('changeuserprivileges/<int:pk>', views.ChangeUser.as_view(), name = 'changeuser' ),

]
