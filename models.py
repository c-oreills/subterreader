from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Document(models.Model):
  """
  A webpage added to the reading list
  """
  url = models.CharField(max_length=255)
  user = models.ForeignKey(User)
  is_read = models.BooleanField()

  def __str__(self):
    return self.url

  def clean(self):
    if '://' not in self.url[:10]:
      self.url = 'http://%s' % self.url
