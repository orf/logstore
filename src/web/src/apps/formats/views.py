from django.views.generic import CreateView, DeleteView, DetailView, UpdateView
from django.views.generic.base import ContextMixin
from .models import Format, Splitter, Field, Transform
from .forms import AddFormatForm, SplitterForm, FieldForm, TransformForm
from django.core.urlresolvers import reverse_lazy


class FormatMixin(ContextMixin):

    def get_context_data(self, **kwargs):
        kwargs["format"] = Format.objects.get(id=self.kwargs["format_id"])
        try:
            kwargs["field"] = Field.objects.get(id=self.kwargs.get("field_id", None))
        except Field.DoesNotExist:
            pass

        try:
            kwargs["transformation"] = Transform.objects.get(id=self.kwargs.get("transform_id", None))
        except Transform.DoesNotExist:
            pass
        return super(FormatMixin, self).get_context_data(**kwargs)


class FormatsListView(CreateView):
    form_class = AddFormatForm
    template_name = "list_formats.html"
    success_url = reverse_lazy("formats:view")

    def get_context_data(self, **kwargs):
        ctx = super(FormatsListView, self).get_context_data(**kwargs)
        ctx["object_list"] = Format.objects.order_by("id").all()
        return ctx


class FormatDeleteView(DeleteView):
    model = Format
    success_url = reverse_lazy("formats:view")
    http_method_names = ["post"]


class FormatDetailView(DetailView):
    model = Format
    template_name = "edit_format.html"


class SplitterView(FormatMixin, UpdateView):
    form_class = SplitterForm
    template_name = "edit_splitter.html"

    def get_object(self, queryset=None):
        try:
            return Splitter.objects.get(format_id=self.kwargs["format_id"])
        except Splitter.DoesNotExist:
            return None

    def form_valid(self, form):
        self.object = form.save(False)
        self.object.format_id = self.kwargs["format_id"]
        self.object.save()
        return super(SplitterView, self).form_valid(form)

    def get_success_url(self):
        return reverse_lazy("formats:edit", args=[self.object.format_id])


class AddFieldView(FormatMixin, UpdateView):
    form_class = FieldForm
    template_name = "edit_field.html"

    def get_object(self, queryset=None):
        try:
            return Field.objects.get(format_id=self.kwargs["format_id"], id=self.kwargs.get("field_id", None))
        except Field.DoesNotExist:
            return None

    def form_valid(self, form):
        self.object = form.save(False)
        self.object.format_id = self.kwargs["format_id"]
        self.object.save()
        return super(AddFieldView, self).form_valid(form)

    def get_success_url(self):
        return reverse_lazy("formats:modify_field", args=[self.object.format_id, self.object.id])


class AddTransformationView(FormatMixin, UpdateView):
    form_class = TransformForm
    template_name = "edit_transformation.html"

    def get_object(self, queryset=None):
        try:
            return Transform.objects.get(field__format__id=self.kwargs["format_id"],
                                         field_id=self.kwargs["field_id"],
                                         id=self.kwargs.get("transform_id", None))
        except Transform.DoesNotExist:
            return None

    def form_valid(self, form):
        self.object = form.save(False)
        self.object.field_id = self.kwargs["field_id"]
        self.object.save()
        return super(AddTransformationView, self).form_valid(form)

    def get_success_url(self):
        return reverse_lazy("formats:modify_field", args=[self.kwargs["format_id"],
                                                          self.object.field_id])