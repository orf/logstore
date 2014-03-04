from django.conf.urls import patterns, url

from .views import EventsView, DeleteEventView, EditEventView, DeleteQueryView, EditEventFilesView


urlpatterns = patterns('',
    url(r'^$', EventsView.as_view(), name='view'),
    url(r'^(?P<event_id>\d+)$', EditEventView.as_view(), name='edit'),
    url(r'^(?P<event_id>\d+)/edit_files$', EditEventFilesView.as_view(), name='edit_files'),
    url(r'^(?P<event_id>\d+)/delete/(?P<query_id>\d+)$',
        DeleteQueryView.as_view(pk_url_kwarg="query_id"), name='delete_query'),
    url(r'^delete/(?P<event_id>\d+)$', DeleteEventView.as_view(pk_url_kwarg="event_id"), name="delete")
)
