from django.views.generic import View
from django.views.generic.detail import SingleObjectMixin
from django.http.response import HttpResponse
from elasticsearch import Elasticsearch
from django.conf import settings
import json
import cPickle
import base64

from ..servers.models import Server
from ..formats.models import Format

es = Elasticsearch(settings.ELASTICSEARCH_URL)


class SearchLogsView(View):
    def get(self, *args, **kwargs):

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


class SerializeFormatView(SingleObjectMixin, View):
    model = Format

    def get(self, request, *args, **kwargs):
        format = self.get_object()
        return HttpResponse(base64.encodestring(cPickle.dumps(format.create_format(),
                                                              protocol=cPickle.HIGHEST_PROTOCOL)), status=200)