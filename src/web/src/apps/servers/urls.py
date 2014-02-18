from django.conf.urls import patterns, url
from .views import ServersView

urlpatterns = patterns('',
    url(r'^$', ServersView.as_view(), name='view'),
)
