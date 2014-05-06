from django.views.generic import CreateView, DeleteView, UpdateView, FormView
from django.views.generic.base import ContextMixin
from django.views.generic.detail import SingleObjectMixin
from django.core.urlresolvers import reverse_lazy

from .models import Format, Field, Transform, FormatStream
from .forms import AddFormatForm, FieldForm, TransformForm, FormatStreamsForm, ModifyFormatForm, TestFormatDataForm

import time


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
    template_name = "formats/list_formats.html"
    success_url = reverse_lazy("formats:view")

    def get_context_data(self, **kwargs):
        ctx = super(FormatsListView, self).get_context_data(**kwargs)
        ctx["object_list"] = Format.objects.order_by("id").all()
        return ctx


class FormatDeleteView(DeleteView):
    model = Format
    success_url = reverse_lazy("formats:view")
    http_method_names = ["post"]


class FormatDetailView(UpdateView):
    form_class = ModifyFormatForm
    model = Format
    template_name = "formats/edit_format.html"

    def get_initial(self):
        return {
            "streams": ", ".join((s.name for s in self.object.streams.all()))
        }

    def form_valid(self, form):
        if "streams" in form.changed_data:
            streams = set(x.strip() for x in form.cleaned_data["streams"].split(","))

            self.object.streams.all().delete()

            FormatStream.objects.bulk_create(
                [FormatStream(name=n, format=self.object) for n in streams]
            )

        return super(FormatDetailView, self).form_valid(form)

    def get_success_url(self):
        return reverse_lazy("formats:edit", args=[self.object.id])


class FormatTestDataView(SingleObjectMixin, FormView):
    form_class = TestFormatDataForm
    model = Format
    template_name = "formats/test_format.html"

    def get_form_kwargs(self):
        kwargs = super(FormatTestDataView, self).get_form_kwargs()
        kwargs["format_id"] = self.kwargs["format_id"]
        return kwargs

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super(FormatTestDataView, self).get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super(FormatTestDataView, self).post(request, *args, **kwargs)

    def form_valid(self, form):
        context = self.get_context_data(form=form)
        extractor = self.get_object().create_format()
        msg = form.cleaned_data["input"]
        t1 = time.time()
        context["extracted_data"] = extractor.process(msg, debug=True)
        context["extraction_speed"] = (time.time() - t1) * 1000 # Get the ms total
        context["split_data"] = extractor.splitter.split(msg)
        return self.render_to_response(context)


class AddFieldView(FormatMixin, UpdateView):
    form_class = FieldForm
    template_name = "formats/edit_field.html"

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
    template_name = "formats/edit_transformation.html"

    def get_object(self, queryset=None):
        try:
            return Transform.objects.get(field__format__id=self.kwargs["format_id"],
                                         field_id=self.kwargs["field_id"],
                                         id=self.kwargs.get("transform_id", None))
        except Transform.DoesNotExist:
            return None

    def form_valid(self, form):
        form.instance.field_id = self.kwargs["field_id"]
        return super(AddTransformationView, self).form_valid(form)

    def get_success_url(self):
        return reverse_lazy("formats:modify_field", args=[self.kwargs["format_id"],
                                                          self.object.field_id])


class EditFormatStreamsView(FormatMixin, SingleObjectMixin, FormView):
    form_class = FormatStreamsForm
    template_name = "formats/edit_format_streams.html"
    model = Format
    pk_url_kwarg = "format_id"

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super(EditFormatStreamsView, self).dispatch(request, *args, **kwargs)



    def get_success_url(self):
        return reverse_lazy("formats:edit", args=[self.get_object().id])


class DeleteTransformView(DeleteView):
    model = Transform
    http_method_names = ["post"]

    def get_queryset(self):
        return self.model.objects.filter(field__id=self.kwargs["field_id"],
                                         field__format_id=self.kwargs["format_id"])

    def get_success_url(self):
        return reverse_lazy("formats:modify_field", args=[self.kwargs["format_id"], self.kwargs["field_id"]])