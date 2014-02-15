from django.views.generic import UpdateView, ListView, DeleteView, DetailView, CreateView
from utils.LogbookContextMixin import PageMixin
from django.http.response import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.conf import settings
import pyelasticsearch


class SuspendServerView(PageMixin, DeleteView):
    """
    I don't delete a server, I merely suspend it
    """
    PAGE_TITLE = "Suspend Server"

    def delete(self, request, *args, **kwargs):
        """
        Calls the delete() method on the fetched object and then
        redirects to the success URL.
        """
        object = self.get_object()
        object.suspended = not object.suspended
        object.save()

        conductor.disconnect_daemon([object.id])

        return HttpResponseRedirect(object.get_absolute_url())


class AddServerView(PageMixin, CreateView):
    PAGE_TITLE = "Add a server"


class ModifyServerView(PageMixin, UpdateView):
    PAGE_TITLE = "Modify Server"

    def form_valid(self, form):
        resp = super(ModifyServerView, self).form_valid(form)

        initial_logfiles_pk = form.initial["logfiles"]
        current_logfiles_id = [s.pk for s in form.cleaned_data["logfiles"]]

        new_logfiles = [lf for lf in form.cleaned_data["logfiles"]
                        if lf.pk not in initial_logfiles_pk]

        removed_logfiles_id = [pk for pk in initial_logfiles_pk
                               if not pk in current_logfiles_id]

        if new_logfiles:
            conductor.add_logfile(self.object.id, [lf for lf in new_logfiles if lf.auto_tail])

        if removed_logfiles_id:
            conductor.remove_logfile(self.object.id, removed_logfiles_id)

        return resp


class ServerDetailsView(PageMixin, DetailView):
    PAGE_TITLE = "View Server"

    def get_context_data(self, **kwargs):
        ctx = super(ServerDetailsView, self).get_context_data(**kwargs)
        ctx["server_id"] = self.object.id
        return ctx


class ServersView(PageMixin, ListView):
    PAGE_TITLE = "Server List"


class DeleteServerView(PageMixin, DeleteView):
    PAGE_TITLE = "Delete Server"

    def delete(self, request, *args, **kwargs):
        obj = self.get_object()
        delete_query = obj.get_search_query()
        # Call super to delete the Server instance
        return_ = super(DeleteServerView, self).delete(request, *args, **kwargs)

        # Disconnect the daemon
        conductor.disconnect_daemon([obj.id])

        # Remove logs
        es = pyelasticsearch.ElasticSearch(settings.ELASTICSEARCH_URL)
        es.delete_by_query("logs", "line", delete_query)

        return return_