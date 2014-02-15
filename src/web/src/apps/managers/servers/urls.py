from django.conf.urls import patterns, url
from django.core.urlresolvers import reverse_lazy
from apps.managers.servers.views import ModifyServerView, ServersView, SuspendServerView,\
    DeleteServerView, ServerDetailsView, AddServerView
from apps.managers.servers.forms import ModifyServerForm, AddServerForm
from apps.managers.servers.models import Server


urlpatterns = patterns('',
                       url(r'^$',
                           ServersView.as_view(
                               model=Server, template_name="list_servers.html"
                           ), name="list"),

                       url(r'add$',
                           AddServerView.as_view(
                               form_class=AddServerForm, template_name="add_server.html"
                           ), name="create"),

                       url(r'view/(?P<server_id>\d+)$',
                           ServerDetailsView.as_view(
                               model=Server,
                               pk_url_kwarg="server_id", template_name="view_server.html"
                           ), name="view"),

                       url(r'view/(?P<server_id>\d+)/modify',
                           ModifyServerView.as_view(
                               model=Server, form_class=ModifyServerForm,
                               pk_url_kwarg="server_id", template_name="modify_server.html"
                           ), name="modify"),

                       url(r'view/(?P<server_id>\d+)/delete$',
                           DeleteServerView.as_view(
                               model=Server,
                               pk_url_kwarg="server_id", template_name="delete_server.html",
                               success_url=reverse_lazy("servers:list")
                           ), name="delete"),

                       url(r'view/(?P<server_id>\d+)/suspend',
                           SuspendServerView.as_view(
                               model=Server,
                               pk_url_kwarg="server_id", template_name="suspend_server.html"
                           ), name="suspend"),
                       )
