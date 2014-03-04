import json
import cPickle
import base64

from django.views.generic import View
from django.views.generic.detail import SingleObjectMixin
from django.http.response import HttpResponse
from django.shortcuts import Http404
from elasticsearch import Elasticsearch
from django.conf import settings

from ..servers.models import Server
from ..formats.models import Format
from ..events.models import Event


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


class SerializeFormatView(View):
    def get(self, request, *args, **kwargs):
        name = self.request.GET.getlist("formats")
        formats = Format.objects.filter(files__name__in=name).exclude(splitter=None).all()

        if not formats:
            raise Http404()

        return HttpResponse(base64.encodestring(cPickle.dumps([f.create_format() for f in formats],
                                                              protocol=cPickle.HIGHEST_PROTOCOL)), status=200)


class EventHitView(SingleObjectMixin, View):
    def get_queryset(self):
        return Event.objects.filter(hash=self.request.GET["HIT"])