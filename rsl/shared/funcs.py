from django.http import HttpResponseForbidden

def admin_required(func):
    def wrapper(request, *args, **kwargs):
        if not request.user.is_superuser:
            return HttpResponseForbidden()
        return func( request, *args, **kwargs)
    return wrapper