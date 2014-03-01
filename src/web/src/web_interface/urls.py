from django.conf.urls import patterns, include, url
from django.views.generic import RedirectView
from django.contrib import admin
admin.autodiscover()

# ToDo: RedirectView() with no / causes it to be displayed in the navigation crumb trail
urlpatterns = patterns('',
    url(r'^$', RedirectView.as_view(pattern_name="dashboard:dashboard"), name="LogBook"),
    url(r'^dashboard/', include('apps.dashboard.urls', namespace="dashboard")),
    url(r'^search/', include('apps.search.urls', namespace="search")),
    url(r'^servers/', include('apps.servers.urls', namespace='servers')),
    url(r'^formats/', include('apps.formats.urls', namespace='formats')),
    url(r'^search/', include('apps.search.urls', namespace='search')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^api/', include('apps.api.urls', namespace="api")),

    url(r'^djangojs/', include('djangojs.urls')),
)
