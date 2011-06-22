from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response
from django.template import RequestContext
from subterreader.models import Document

@login_required
def manage(request):
  documents_list = Document.objects.filter(user=request.user).all()
  return render_to_response('subterreader/manage.html', {'documents_list': documents_list})

@login_required
def settings(request):
  return HttpResponse('User settings')

@login_required
def read(request):
  documents_list = Document.objects.filter(user=request.user).all()
  return render_to_response('subterreader/read.html', {'documents_list': documents_list}, RequestContext(request))

