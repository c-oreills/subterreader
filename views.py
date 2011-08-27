from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from subterreader.view_decorators import process_read_pages_cookie
from subterreader.forms import AddWebpageForm
from subterreader.models import Webpage

def main(request):
    if request.user.is_authenticated():
        return manage(request)
    else:
        return render(request, 'subterreader/intro.html.haml')

@login_required
@process_read_pages_cookie
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
@process_read_pages_cookie
def settings(request):
    return HttpResponse('User settings')

@login_required
@process_read_pages_cookie
def read(request):
    if request.is_ajax():
        # Token response for AJAX polling
        return HttpResponse('live')
    else:
        webpages_list = Webpage.objects.filter(user=request.user, is_read=False).all()
        return render(request, 'subterreader/read.html.haml', {'webpages_list': webpages_list})

def sample(request):
    sample_urls = ('http://norvig.com/21-days.html', 'http://www.paulgraham.com/avg.html', 'http://www.ccs.neu.edu/home/shivers/autoweapons.html')
    webpages_list = [Webpage(url=url) for url in sample_urls]
    return render(request, 'subterreader/read.html.haml', {'webpages_list': webpages_list})
