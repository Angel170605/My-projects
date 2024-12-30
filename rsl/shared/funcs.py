from django.http import HttpResponseForbidden
from datetime import date


def admin_required(func):
    def wrapper(request, *args, **kwargs):
        if not request.user.is_superuser:
            return HttpResponseForbidden()
        return func( request, *args, **kwargs)
    return wrapper

def get_player_age(birthdate: date) -> int:
    now = date.today()

    TODAY = now.day
    MONTH = now.month
    YEAR = now.year

    if birthdate.month > MONTH:
        return YEAR - birthdate.year - 1
    elif birthdate.month == MONTH:
        if birthdate.day > TODAY:
            return YEAR - birthdate.year - 1
        else:
            return YEAR - birthdate.year
    else:
        return YEAR - birthdate.year