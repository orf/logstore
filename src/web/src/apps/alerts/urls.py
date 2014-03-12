from django.conf.urls import patterns, url

from .views import AlertsView, DeleteAlertView, EditAlertView, DeleteAlertConditionView, AddContactView,\
    DeleteContactView, AddAlertCondition


urlpatterns = patterns('',
    url(r'^$', AlertsView.as_view(template_name="list_alerts.html"), name='view'),
    url(r'^(?P<alert_id>\d+)$', EditAlertView.as_view(pk_url_kwarg="alert_id",
                                                      template_name="edit_alert.html"), name='edit'),
    url(r'^(?P<alert_id>\d+)/condition/add/(?P<condition_type>\w+)$', AddAlertCondition.as_view(),name="add_condition"),
    url(r'^(?P<alert_id>\d+)/condition/(?P<condition_id>\d+)$',
        DeleteAlertConditionView.as_view(pk_url_kwarg="condition_id"), name="delete_condition"),

    url(r'^(?P<alert_id>\d+)/contact/add/(?P<contact_type>\w+)$', AddContactView.as_view(), name="add_contact"),
    url(r'^(?P<alert_id>\d+)/contact/delete/(?P<contact_id>\d+)$',
        DeleteContactView.as_view(pk_url_kwarg="contact_id"), name="delete_contact"),
    url(r'^(?P<alert_id>\d+)/delete$', DeleteAlertView.as_view(pk_url_kwarg="alert_id"), name='delete'),
)