from django.views.generic import TemplateView
from elasticsearch import Elasticsearch
from django.conf import settings
from ..servers.models import Server

es = Elasticsearch(settings.ELASTICSEARCH_URL)


class SearchView(TemplateView):
    def get_context_data(self, **kwargs):
        ctx = super(SearchView, self).get_context_data(**kwargs)
        ctx["query"] = self.request.GET.get("query", "")
        ctx["servers"] = Server.objects.all()

        results = es.search("logs",
                            "line",
                            {
                                "query": {
                                    "match_all": {}
                                },
                                "facets": {
                                    "stream_names": {
                                        "terms": {
                                            "field": "stream_name"
                                        }
                                    }
                                }
                            },
                            size=0)
        ctx["streams"] = [x["term"] for x in results["facets"]["stream_names"]["terms"]]
        return ctx

