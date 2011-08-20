from django.core.exceptions import ObjectDoesNotExist
from django.utils.decorators import available_attrs
from functools import wraps
from subterreader.models import Webpage
from urllib import unquote

def mark_read_pages(view_func):
    """
    Wraps view functions, checks for read_webpages cookie in request and marks
    specified webpages as read. Deletes the cookie afterwards.
    """
    @wraps(view_func, assigned=available_attrs(view_func))
    def mark_read(request, *args, **kwargs):
        if 'read_webpages' in request.COOKIES:
            read_webpages = set(unquote(request.COOKIES['read_webpages']).split(','))
            for webpage_id in read_webpages:
                try:
                    webpage_id = int(webpage_id, 10)
                except ValueError:
                    print 'Could not convert %s to int' % webpage_id
                    continue
                try: 
                    webpage = Webpage.objects.filter(user=request.user).get(id=webpage_id)
                except ObjectDoesNotExist:
                    print 'Could not find Webpage with id %s' % webpage_id
                    continue # TODO: Proper logging of unsuccessful lookups
                if not webpage.is_read:
                    webpage.is_read = True
                    webpage.save() # TODO: Make this a bulk transaction
            response = view_func(request, *args, **kwargs)
            response.delete_cookie('read_webpages')
            return response
        else:
            return view_func(request, *args, **kwargs)
    return mark_read
