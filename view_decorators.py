from django.utils.decorators import available_attrs
from subterreader.view_helpers import mark_webpages_as_read
from functools import wraps
from urllib import unquote

def process_read_pages_cookie(view_func):
    """
    Wraps view functions, checks for read_webpages cookie in request and marks
    specified webpages as read. Deletes the cookie afterwards.
    """
    @wraps(view_func, assigned=available_attrs(view_func))
    def mark_read(request, *args, **kwargs):
        if 'read_webpages' in request.COOKIES:
            read_webpages = set(unquote(request.COOKIES['read_webpages']).split(','))
            mark_webpages_as_read(read_webpages, request.user)
            response = view_func(request, *args, **kwargs)
            response.delete_cookie('read_webpages')
            return response
        else:
            return view_func(request, *args, **kwargs)
    return mark_read
