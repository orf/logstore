from django.conf.urls import patterns, url
from apps.search.views import SearchView

urlpatterns = patterns('',
    url(r'^$', SearchView.as_view(template_name="search.html"), name='dashboard'),
)
