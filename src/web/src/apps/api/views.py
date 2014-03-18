import json

from django.views.generic import View
from django.http.response import HttpResponse
from elasticsearch import Elasticsearch
from django.conf import settings
from django.shortcuts import get_object_or_404

from ..formats.models import Format
from ..servers.models import Server


es = Elasticsearch(settings.ELASTICSEARCH_URL)


class GetLogFileNamesView(View):
    def get(self, *args, **kwargs):
        results = es.search("logs", "line", {"query": {"match_all": {}},
                                             "facets": {"file_name": {"terms": {"field": "file_name"}}}}, size=0)
        return HttpResponse(json.dumps(
            [x["term"] for x in results["facets"]["file_name"]["terms"]]
        ), status=200, content_type="text/json")


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


class GetRandomLogMessageView(View):
    def get(self, request, *args, **kwargs):
        if "format_id" in request.GET:
            format = get_object_or_404(Format, id=request.GET["format_id"])
            query = {
                "query_string": {
                    "query": format.get_stream_name_query()
                }
            }
        else:
            query = {
                "match_all": {}
            }

        results = es.search("logs",
                            "line",
                            {
                                "query": query,
                                "sort": {
                                    "_script": {
                                        "script": "Math.random()",
                                        "type": "number",
                                        "params":{},
                                        "order": "asc"
                                    }
                                }
                            },
                            size=1)

        hits = results["hits"]["hits"]
        msg = hits[0]["_source"]["message"] if len(hits) else ""
        return HttpResponse(msg, status=200, content_type="text/plain")