from django.conf.urls import patterns, url

from .views import AlertsView, DeleteAlertView, EditAlertView


urlpatterns = patterns('',
    url(r'^$', AlertsView.as_view(template_name="list_alerts.html"), name='view'),
    url(r'^(?P<alert_id>\d+)$', EditAlertView.as_view(pk_url_kwarg="alert_id",
                                                      template_name="edit_alert.html"), name='edit'),
    url(r'^(?P<alert_id>\d+)/delete$', DeleteAlertView.as_view(pk_url_kwarg="alert_id"), name='delete'),
)