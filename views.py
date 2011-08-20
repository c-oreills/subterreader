from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from subterreader.view_decorators import mark_read_pages
from subterreader.forms import AddWebpageForm
from subterreader.models import Webpage

@login_required
@mark_read_pages
def manage(request):
    if request.method == 'POST':
        form = AddWebpageForm(request.POST)
        # TODO: Ensure urls field is cleaned
        if form.is_valid():
            webpages, errors = form.create_webpages()
            for webpage in webpages:
                webpage.user = request.user
                webpage.save()
            for error in errors:
                pass # TODO: Handle errors in a meaningful way, display to user etc
    else:
        form = AddWebpageForm()
    context = {
        'webpages_list': Webpage.objects.filter(user=request.user, is_read=False).all(),
        'form': form,
        }
    return render(request, 'subterreader/manage.html.haml', context)

@login_required
@mark_read_pages
def settings(request):
    return HttpResponse('User settings')

@login_required
@mark_read_pages
def read(request):
    webpages_list = Webpage.objects.filter(user=request.user, is_read=False).all()
    return render(request, 'subterreader/read.html.haml', {'webpages_list': webpages_list})
