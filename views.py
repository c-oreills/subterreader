from django.http import HttpResponse

def manage(request):
  return HttpResponse("A list of docs that have yet to be read")

def settings(request):
  return HttpResponse("User settings")

def read(request):
  return HttpResponse("iFrames full of docs on reading list")
