from django.views.generic import View
from django.http.response import HttpResponse
from elasticsearch import Elasticsearch
from django.conf import settings
import json

from ..servers.models import Server


class SearchLogsView(View):
    def get(self, *args, **kwargs):
        es = Elasticsearch(settings.ELASTICSEARCH_URL)
        results = es.search(
            body={
                "query": {
                    "query_string": {
                        "query": self.request.GET["query"]
                    }
                },
                "highlight": {
                    "fields": {
                        "message": {}
                    }
                },
                "sort": {
                    "read_time": "desc"
                }
            },
            index="logs",
            doc_type="line",
            size=self.request.GET.get("size", 25),
            from_=self.request.GET.get("from", 0)
        )

        return HttpResponse(json.dumps(results), status=200, content_type="text/json")


# ToDo: Add caching
class ServerAuthView(View):
    def get(self, request, *args, **kwargs):

        try:
            server = Server.objects.get(ip=request.GET["ip"])
        except Server.DoesNotExist:
            return HttpResponse("", status=401)
        else:
            return HttpResponse(str(server.id), status=200)
