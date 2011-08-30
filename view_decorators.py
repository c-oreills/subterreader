from django.utils.decorators import available_attrs
from subterreader.view_helpers import mark_webpages_as_read, add_urls_to_list
from functools import wraps
from urllib import unquote


def make_process_cookie_wrapper(cookie_name, cookie_func):
    def process_cookie_wrapper(view_func):
        """
        Wraps view functions, checks for cookie_name in request's cookies,
        splits into a set and calls cookie_func on it. Deletes the cookie
        afterwards.
        """
        @wraps(view_func, assigned=available_attrs(view_func))
        def process_cookie(request, *args, **kwargs):
            if cookie_name in request.COOKIES:
                cookie_values = set(unquote(request.COOKIES[cookie_name]).split(','))
                cookie_func(cookie_values, request.user)
                response = view_func(request, *args, **kwargs)
                response.delete_cookie(cookie_name)
                return response
            else:
                return view_func(request, *args, **kwargs)
        return process_cookie
    return process_cookie_wrapper

process_read_pages_cookie = make_process_cookie_wrapper('read_webpages', mark_webpages_as_read)
process_add_url_cookie = make_process_cookie_wrapper('add_urls', add_urls_to_list)

def process_cookies(fn):
    return process_read_pages_cookie(
            process_add_url_cookie(fn))
