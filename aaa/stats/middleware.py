from django.core.mail import send_mail
from accounts.models import User
from .models import RequestObj, PageObj
from django.conf import settings
from urllib.parse import urljoin

class SimpleMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.
        if request.user.is_staff:
            user = request.user
        else:
            user = None
        if request.user == User.objects.get(email = 'suryaveda@hotmail.com'):

            x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
            if x_forwarded_for:
                ip = x_forwarded_for.split(',')[0]
            else:
                ip = request.META['REMOTE_ADDR']
        try:
            print(ip)
        except Exception as e:
            ip = ''

        path = urljoin(settings.DOMAIN_NAME, request.path)
            #send_mail("Below are the links to ip addr of client.", "Kindly press the below link or copy and paste it in browser to join the lecture \n \n {0}".format(ip), settings.EMAIL_HOST_USER, [request.user.email], fail_silently=True)

        response = self.get_response(request)
        
        if response.status_code == 200:
            x = RequestObj.objects.create()
            if user:
                x.user = user
            try:
                page = PageObj.objects.get(url = path)
            except Exception as e:
                page = PageObj.objects.create(url=path)
            x.location = ip
            x.page = page
            x.save()




        # Code to be executed for each request/response after
        # the view is called.

        return response
