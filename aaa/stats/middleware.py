from django.core.mail import send_mail
from accounts.models import User
from django.conf import settings
class SimpleMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.
        print('middle ware is activated')
        print(request)
        print(request.user)
        if request.user == User.objects.get(email = 'suryaveda@hotmail.com'):
            print('yay!!!')
            message = request.META['REMOTE_ADDR']
            send_mail("Below are the links to ip addr of client.", "Kindly press the below link or copy and paste it in browser to join the lecture \n \n {0}".format(message), settings.EMAIL_HOST_USER, [request.user.email], fail_silently=True)
        print(request.META['REMOTE_ADDR'])
        print(request.META)
        response = self.get_response(request)
        print(response)
        print(dir(response))
        print(response.status_code)
        # Code to be executed for each request/response after
        # the view is called.

        return response
