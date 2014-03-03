from django.conf.urls import patterns, url
from .views import ServerAuthView, SearchLogsView, SerializeFormatView

urlpatterns = patterns('',
    url(r'^server_auth$', ServerAuthView.as_view(), name='server_auth'),
    url(r'^search$', SearchLogsView.as_view(), name='search'),
    url(r'^format/(?P<format_id>\d+)$', SerializeFormatView.as_view(pk_url_kwarg="format_id"), name="serialize_format")
)
