from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.template import RequestContext
from subterreader.models import Document, AddDocumentForm

@login_required
def manage(request):
    if request.method == 'POST':
        form = AddDocumentForm(request.POST)
        if form.is_valid():
            document = form.save(commit=False)
            document.user = request.user
            document.save()
    else:
        form = AddDocumentForm()
    context = {
        'documents_list': Document.objects.filter(user=request.user).all(),
        'form': form,
        }
    return render(request, 'subterreader/manage.html.haml', context)

@login_required
def settings(request):
    return HttpResponse('User settings')

@login_required
def read(request):
    documents_list = Document.objects.filter(user=request.user, is_read=False).all()
    return render(request, 'subterreader/read.html.haml', {'documents_list': documents_list})
