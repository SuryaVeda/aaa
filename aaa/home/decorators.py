from django.core.exceptions import PermissionDenied


def staff_required(function):
    def wrap(request, args=None, **kwargs):
        if request.user.is_staff == True:
            return function(request, **kwargs)
        else:
            raise PermissionDenied
    return wrap