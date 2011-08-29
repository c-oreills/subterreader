from django.core.exceptions import ObjectDoesNotExist
from subterreader.models import Webpage

def mark_webpages_as_read(webpage_ids, user):
    """
    Takes a list of webpage_ids, converts them to ints and marks them as read
    """
    for webpage_id in webpage_ids:
        try:
            webpage_id = int(webpage_id, 10)
        except ValueError:
            print 'Could not convert %s to int' % webpage_id
            continue
        try: 
            webpage = Webpage.objects.filter(user=user).get(id=webpage_id)
        except ObjectDoesNotExist:
            print 'Could not find Webpage with id %s' % webpage_id
            continue # TODO: Proper logging of unsuccessful lookups
        if not webpage.is_read:
            webpage.is_read = True
            webpage.save() # TODO: Make this a bulk transaction

def add_urls_to_list(urls, user):
    for url in urls:
        webpage = Webpage(url=url, user=user)
        try:
            webpage.full_clean()
        except Exception, e:
            raise e # TODO: Handle validation errors properly
        webpage.save()
