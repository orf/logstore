from django.conf.urls import patterns, url

from .views import Dashboard


urlpatterns = patterns('',
    url(r'^$', Dashboard.as_view(template_name="dashboard/home.html"), name='dashboard'),
)
