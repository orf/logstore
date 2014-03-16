from django.views.generic import CreateView, DeleteView, DetailView
from django.core.urlresolvers import reverse_lazy, reverse
from django.shortcuts import get_object_or_404

from .models import Alert, AlertCondition, AlertContact
from .forms import AddAlertForm, AddAlertConditionEventTriggeredForm, AddAlertConditionBucketCountForm,\
    AddAlertEmailContactForm, AddAlertTextContactForm, AddAlertPushBulletContactForm, AddAlertConditionPercentageForm,\
    AddAlertConditionStatsForm


class AlertMixin(object):
    def get_context_data(self, **kwargs):
        ctx = super(AlertMixin, self).get_context_data(**kwargs)
        ctx["alert"] = get_object_or_404(Alert, id=self.kwargs["alert_id"])
        return ctx


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


class AddAlertCondition(AlertMixin, CreateView):
    template_name = "add_alert_form_display.html"

    def get_form_class(self):
        return {"count": AddAlertConditionBucketCountForm,
                "trigger": AddAlertConditionEventTriggeredForm,
                "stats": AddAlertConditionStatsForm,
                "percentage": AddAlertConditionPercentageForm}[self.kwargs["condition_type"]]

    def form_valid(self, form):
        form.instance.alert_id = self.kwargs["alert_id"]
        return super(AddAlertCondition, self).form_valid(form)

    def get_success_url(self):
        return reverse("alerts:edit", args=[self.kwargs["alert_id"]])


class DeleteAlertConditionView(DeleteView):
    model = AlertCondition

    def get_queryset(self):
        return self.model.objects.filter(alert_id=self.kwargs["alert_id"])

    def get_success_url(self):
        return reverse("alerts:edit", args=[self.kwargs["alert_id"]])


class AddContactView(AlertMixin, CreateView):
    template_name = "add_alert_form_display.html"

    def get_form_class(self):
        return {
            "email": AddAlertEmailContactForm,
            "text": AddAlertTextContactForm,
            "push": AddAlertPushBulletContactForm,
        }[self.kwargs["contact_type"]]

    def form_valid(self, form):
        form.instance.alert_id = self.kwargs["alert_id"]
        if hasattr(form, "modify_instance"):
            form.modify_instance()
        return super(AddContactView, self).form_valid(form)

    def get_success_url(self):
        return reverse("alerts:edit", args=[self.kwargs["alert_id"]])


class DeleteContactView(DeleteView):
    model = AlertContact

    def get_success_url(self):
        return reverse("alerts:edit", args=[self.kwargs["alert_id"]])