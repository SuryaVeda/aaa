from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect

def staff_required(function):
    def wrap(request, args=None, **kwargs):
        if request.user.is_authenticated == True:
            return function(request, **kwargs)
        else:
            return redirect('accounts:staff')
    return wrap
