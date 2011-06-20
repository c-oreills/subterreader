from django.http import HttpResponse
from django.contrib.auth.decorators import login_required


@login_required
def manage(request):
  return HttpResponse('%s\'s list of docs that have yet to be read' % request.user.username)

@login_required
def settings(request):
  return HttpResponse('User settings')

@login_required
def read(request):
  return HttpResponse('iFrames full of docs on reading list')

