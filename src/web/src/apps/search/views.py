from django.views.generic import TemplateView
from pyelasticsearch import ElasticSearch
from django.conf import settings
from ..servers.models import Server


class SearchView(TemplateView):
    def get_context_data(self, **kwargs):
        ctx = super(SearchView, self).get_context_data(**kwargs)
        ctx["query"] = self.request.GET.get("query", "")
        ctx["servers"] = Server.objects.all()
        return ctx

