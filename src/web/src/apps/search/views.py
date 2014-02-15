from django.views.generic import TemplateView
from pyelasticsearch import ElasticSearch
from django.conf import settings


class SearchView(TemplateView):
    def get_context_data(self, **kwargs):
        ctx = super(SearchView, self).get_context_data(**kwargs)
        ctx["query"] = self.request.GET.get("query", "")
        return ctx

