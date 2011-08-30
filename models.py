from django.db import models
from django.contrib.auth.models import User

class UnreadByAgeManager(models.Manager):
    def get_query_set(self):
        # Return oldest first (assumes lower ids are older)
        return super(UnreadByAgeManager, self).get_query_set().filter(is_read=False).order_by('id')

class Webpage(models.Model):
    """
    A webpage added to the reading list
    """
    url = models.URLField(verify_exists=False, max_length=255)
    user = models.ForeignKey(User)
    is_read = models.BooleanField(default=False)

    unread_by_age = UnreadByAgeManager()

    def __unicode__(self):
        return self.url

    def clean(self):
        if '://' not in self.url[:10]:
            self.url = 'http://%s' % self.url


