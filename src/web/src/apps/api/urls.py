from django.conf.urls import patterns, url
from .views import ServerAuthView, SearchLogsView


urlpatterns = patterns('',
    url(r'^server_auth$', ServerAuthView.as_view(), name='server_auth'),
    url(r'^search$', SearchLogsView.as_view(), name='search')
)
