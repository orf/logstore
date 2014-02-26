from django.views.generic import CreateView, DeleteView
from django.core.urlresolvers import reverse_lazy
from .models import Server
from .forms import AddServerForm


class ServersView(CreateView):
    form_class = AddServerForm
    template_name = "servers.html"
    success_url = reverse_lazy("servers:view")

    def get_context_data(self, **kwargs):
        ctx = super(ServersView, self).get_context_data(**kwargs)
        ctx["object_list"] = Server.objects.order_by("id").all()
        return ctx


class DeleteServerView(DeleteView):
    model = Server
    success_url = reverse_lazy("servers:view")
    http_method_names = ["post"]