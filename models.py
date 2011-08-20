from django.db import models
from django.contrib.auth.models import User

class Webpage(models.Model):
    """
    A webpage added to the reading list
    """
    url = models.URLField(verify_exists=False, max_length=255)
    user = models.ForeignKey(User)
    is_read = models.BooleanField(default=False)

    def __unicode__(self):
        return self.url

    def clean(self):
        if '://' not in self.url[:10]:
            self.url = 'http://%s' % self.url


