from django.conf.urls import patterns, url

from .views import ServerAuthView, SearchLogsView, GetLogFileNamesView, GetRandomLogMessageView


urlpatterns = patterns('',
    url(r'^server_auth$', ServerAuthView.as_view(), name='server_auth'),
    url(r'^search$', SearchLogsView.as_view(), name='search'),
    url(r'^get_log_files$', GetLogFileNamesView.as_view(), name='get_log_file_names'),
    url(r'^random_message$', GetRandomLogMessageView.as_view(), name="random_log_message")
)