from django.conf.urls import patterns, url

from .views import FormatsListView, FormatDeleteView, FormatDetailView,\
    AddFieldView, AddTransformationView, FormatTestDataView, DeleteTransformView


urlpatterns = patterns('',
    url(r'^$', FormatsListView.as_view(), name='view'),
    url(r'^delete/(?P<format_id>\d+)$', FormatDeleteView.as_view(pk_url_kwarg="format_id"), name="delete"),

    url(r'^(?P<format_id>\d+)$', FormatDetailView.as_view(pk_url_kwarg="format_id"), name="edit"),
    url(r'^(?P<format_id>\d+)/test$', FormatTestDataView.as_view(pk_url_kwarg="format_id"), name="test"),
    url(r'^(?P<format_id>\d+)/field$', AddFieldView.as_view(), name="add_field"),
    url(r'^(?P<format_id>\d+)/field/(?P<field_id>\d+)$', AddFieldView.as_view(), name="modify_field"),
    url(r'^(?P<format_id>\d+)/field/(?P<field_id>\d+)/transform$',
        AddTransformationView.as_view(), name="add_transformation"),
    url(r'^(?P<format_id>\d+)/field/(?P<field_id>\d+)/transform/(?P<transform_id>\d+)$',
        AddTransformationView.as_view(), name="modify_transformation"),
    url(r'^(?P<format_id>\d+)/field/(?P<field_id>\d+)/transform/(?P<transform_id>\d+)/delete$',
        DeleteTransformView.as_view(pk_url_kwarg="transform_id"), name="delete_transformation"),
)
