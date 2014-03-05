from django.views.generic import DeleteView, CreateView, FormView
from django.core.urlresolvers import reverse_lazy
from django.shortcuts import get_object_or_404
from django.views.generic.detail import SingleObjectMixin

from .models import Event, EventQuery, EventFile
from .forms import AddEventForm, AddEventQueryForm, EventFilesForm


class EventsView(CreateView):
    template_name = "events.html"
    success_url = reverse_lazy("events:view")
    form_class = AddEventForm

    def get_context_data(self, **kwargs):
        ctx = super(EventsView, self).get_context_data(**kwargs)
        ctx["object_list"] = Event.objects.order_by("id").all()
        return ctx


class EditEventView(CreateView):
    model = EventQuery
    template_name = "edit_event.html"
    form_class = AddEventQueryForm

    def get_context_data(self, **kwargs):
        ctx = super(EditEventView, self).get_context_data(**kwargs)
        ctx["event"] = get_object_or_404(Event, id=self.kwargs["event_id"])
        ctx["object_list"] = EventQuery.objects.filter(event_id=self.kwargs["event_id"]).order_by("id").all()
        return ctx

    def form_valid(self, form):
        form.instance.event_id = self.kwargs["event_id"]
        return super(EditEventView, self).form_valid(form)

    def get_success_url(self):
        return reverse_lazy("events:edit", args=[self.object.event_id])


class DeleteQueryView(DeleteView):
    model = EventQuery
    http_method_names = ["post"]

    def get_queryset(self):
        return self.model.objects.filter(event_id=self.kwargs["event_id"], id=self.kwargs["query_id"])

    def get_success_url(self):
        return reverse_lazy("events:edit", args=[self.kwargs["event_id"]])


class DeleteEventView(DeleteView):
    model = Event
    success_url = reverse_lazy("events:view")
    http_method_names = ["post"]


class EditEventFilesView(SingleObjectMixin, FormView):
    form_class = EventFilesForm
    template_name = "edit_event_files.html"
    model = Event
    pk_url_kwarg = "event_id"

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super(EditEventFilesView, self).dispatch(request, *args, **kwargs)

    def get_initial(self):
        return {
            "files": ", ".join((f.name for f in self.object.files.all()))
        }

    def form_valid(self, form):
        event_queries = list(self.object.queries.all())
        self.object.queries.all().delete()

        files = set(x.strip() for x in form.cleaned_data["files"].split(","))

        self.object.files.all().delete()

        EventFile.objects.bulk_create(
            [EventFile(name=n, event=self.object) for n in files]
        )

        for ev in event_queries:
            ev.id = None
            ev.save()

        return super(EditEventFilesView, self).form_valid(form)

    def get_success_url(self):
        return reverse_lazy("events:edit", args=[self.get_object().id])