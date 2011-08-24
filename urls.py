from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns('',
    (r'^$', 'subterreader.views.main'),
    (r'^read/$', 'subterreader.views.read'),
    (r'^settings/$', 'subterreader.views.settings'),
    (r'^sample/$', 'subterreader.views.sample'),
)
