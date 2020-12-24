from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
path('signin', views.login_view, name = 'login' ),
path('signup/staff_signup', views.SignupView.as_view(), name='staff' ),
path('signup/<str:email>/<str:username>', views.SignupView.as_view(), name = 'commonsignup'),
path('signout', views.user_signout, name = 'logout' ),
path('profile', views.MyProfile.as_view(), name = 'myprofile' ),
path('changeuserprivileges/<int:pk>', views.ChangeUser.as_view(), name = 'changeuser' ),
path('reset-your-password', views.PasswordReset.as_view(), name = 'password_reset_form' ),
path('passreset', views.PasswordReset.as_view() ),

]
#urlpatterns +=[path('passreset/<str:{0}>?passwordreset=true'.format(i.reset), views.PasswordReset.as_view()) for i in User.objects.all()]
