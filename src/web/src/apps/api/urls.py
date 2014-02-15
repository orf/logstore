from django.conf.urls import patterns, url
from apps.api.views import ServerAuthView, ServerLogFilesView, GetNodeInfo,\
    GetLogMessagesView, SearchLogsView


urlpatterns = patterns('',
    url(r'^get_node_info$', GetNodeInfo.as_view(), name="get_node_info"),
    url(r'^server_auth$', ServerAuthView.as_view(), name='server_auth'),
    url(r'^get_log_files$', ServerLogFilesView.as_view(), name="get_log_files"),
    url(r'^get_last_messages$', GetLogMessagesView.as_view(), name="get_last_messages"),
    url(r'^search$', SearchLogsView.as_view(), name='search'),
)
