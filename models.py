from django.db import models

# Create your models here.
class Document(models.Model):
  """
  A webpage added to the reading list
  """
  url = models.CharField()
  user = models.ForeignKeyField(User)
  is_read = models.BooleanField()
