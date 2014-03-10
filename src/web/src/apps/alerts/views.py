from django.views.generic import CreateView, DeleteView, DetailView
from django.core.urlresolvers import reverse_lazy

from .models import Alert
from .forms import AddAlertForm


class AlertsView(CreateView):
    success_url = reverse_lazy("alerts:view")
    form_class = AddAlertForm

    def get_context_data(self, **kwargs):
        ctx = super(AlertsView, self).get_context_data(**kwargs)
        ctx["object_list"] = Alert.objects.order_by("id").all()
        return ctx


class DeleteAlertView(DeleteView):
    success_url = reverse_lazy("alerts:view")
    model = Alert


class EditAlertView(DetailView):
    model = Alert