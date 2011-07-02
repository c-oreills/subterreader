from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns('',
    (r'^$', 'subterreader.views.manage'),
    (r'^read/$', 'subterreader.views.read'),
    (r'^settings/$', 'subterreader.views.settings'),
)
