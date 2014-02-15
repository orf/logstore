from django.conf.urls import patterns, url
from apps.dashboard.views import Dashboard

urlpatterns = patterns('',
    url(r'^$', Dashboard.as_view(template_name="home.html"), name='dashboard'),
)
