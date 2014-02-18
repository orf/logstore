from django.views.generic import View
from django.http.response import HttpResponse
#from apps.managers.servers.models import Server
from pyelasticsearch import ElasticSearch
from django.conf import settings
from django.http.response import HttpResponseForbidden
import json
import ipaddr


class LoopBackOnlyMixin(object):
    def dispatch(self, request, *args, **kwargs):

        ip = request.META['REMOTE_ADDR']

        if not ipaddr.IP(ip).IsLoopback:
            return HttpResponseForbidden("Unauthorized")

        return super(LoopBackOnlyMixin, self).dispatch(request, *args, **kwargs)


class BaseRestrictedAPIView(LoopBackOnlyMixin, View):
    @staticmethod
    def get_server(ip):
        return Server.objects.exclude(suspended=True).get(ip=ip)

    @staticmethod
    def get_server_by_id(id):
        return Server.objects.exclude(suspended=True).get(id=id)


class SearchLogsView(View):
    def get(self, *args, **kwargs):
        es = ElasticSearch(settings.ELASTICSEARCH_URL)
        results = es.search(
            {
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
                },
                "facets": {
                    "date_graph": {
                        "date_histogram": {
                            "field": "read_time",
                            "interval": "day"
                        }
                    }
                }
            },
            index="logs",
            doc_type="line",
            size=self.request.GET.get("size", 25),
            es_from=self.request.GET.get("from", 0)
        )

        return HttpResponse(json.dumps(results), status=200, content_type="text/json")


class GetLogMessagesView(BaseRestrictedAPIView):
    def get(self, request, *args, **kwargs):
        es = ElasticSearch(settings.ELASTICSEARCH_URL)

        if "server" in request.GET:
            obj = self.get_server_by_id(request.GET["server"])
        else:
            obj = self.get_logfile_by_id(request.GET["logfile"])

        size = request.GET.get("max", 10)

        search_result = es.search(obj.get_search_query(), size=size, index="logs", es_sort="read_time:desc")

        return HttpResponse(json.dumps(search_result["hits"]["hits"]),
                            status=200, content_type="text/json")


class GetNodeInfo(BaseRestrictedAPIView):
    def get(self, request, *args, **kwargs):
        server = self.get_server(request.GET["ip"])

        return HttpResponse(json.dumps({"id": server.id,
                                        "name": server.name,
                                        "token": server.install_token.token}),
                            status=200, content_type="text/json")


# ToDo: Add caching
class ServerAuthView(BaseRestrictedAPIView):
    def get(self, request, *args, **kwargs):
        try:
            self.get_server(request.GET["ip"])
        except Exception:
            return HttpResponse("", status=401)
        else:
            return HttpResponse("", status=200)


class ServerLogFilesView(BaseRestrictedAPIView):
    def get(self, request, *args, **kwargs):
        try:
            server = self.get_server_by_id(request.GET["id"])
        except Exception:
            return HttpResponse("Server not found", status=401)

        log_files = [(lf.id, lf.name, lf.path) for lf in server.logfiles.exclude(auto_tail=False)]

        return HttpResponse(json.dumps(log_files),
                            status=200, content_type="text/json")

