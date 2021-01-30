from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect

def staff_required(function):
    def wrap(request, args=None, **kwargs):
        if request.user.is_authenticated == True:
            return function(request, **kwargs)
        else:
            return redirect('accounts:staff')
    return wrap

def admin_required(function):
    def wrap(request, args=None, **kwargs):
        if request.user.is_authenticated and request.user.is_admin:
            return function(request, **kwargs)
        else:
            return redirect('accounts:staff')
    return wrap
