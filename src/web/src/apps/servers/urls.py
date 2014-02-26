from django.conf.urls import patterns, url
from .views import ServersView, DeleteServerView

urlpatterns = patterns('',
    url(r'^$', ServersView.as_view(), name='view'),
    url(r'^delete/(?P<id>\d+)', DeleteServerView.as_view(pk_url_kwarg="id"), name="delete")
)
