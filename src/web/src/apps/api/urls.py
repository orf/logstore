from django.conf.urls import patterns, url

from .views import ServerAuthView, SearchLogsView, SerializeFormatView, EventHitView


urlpatterns = patterns('',
    url(r'^server_auth$', ServerAuthView.as_view(), name='server_auth'),
    url(r'^search$', SearchLogsView.as_view(), name='search'),
    url(r'^get_formats$', SerializeFormatView.as_view(), name="get_formats"),
    url(r'^got_event_hit', EventHitView.as_view(), name="got_event_hit")
)
