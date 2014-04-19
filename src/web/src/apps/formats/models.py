from django.db import models
from logstore.extractor.base import Format as ExtractorFormat, Field as ExtractorField, FieldSource
from logstore.extractor.register import registry
from django.core.exceptions import ValidationError
import string


def no_spaces_validator(value):
    for char in string.whitespace:
        if char in value:
            raise ValidationError("Must not contain whitespace")


def no_reserved_names_validator(value):
    if value in ("field_errors",):
        raise ValidationError("%s is a reserved name, please choose another" % value)


splitter_choices = registry.get_choices("splitter")


class Format(models.Model):
    name = models.CharField(max_length=255)

    splitter_type = models.CharField(choices=splitter_choices, default=splitter_choices[0][0], max_length=255)
    splitter_args = models.CharField(max_length=255, null=True, blank=True)

    def create_format(self):
        return ExtractorFormat(
            splitter=self.get_splitter(),
            fields=[field.get_field() for field in self.fields.all()]
        )

    def get_stream_name_query(self, postfix=""):
        names = self.streams.values_list("name")
        if not names:
            return ""
        return " OR ".join('(stream_name:"%s")' % name for name in names) + postfix

    def get_stream_name_filter_query(self):
        return {"terms": {"stream_name": list(self.streams.values_list("name", flat=True))}}

    def get_splitter(self):
        return registry.get_by_name("splitter", self.splitter_type)(self.splitter_args)


class FormatStream(models.Model):
    name = models.CharField(max_length=250)
    format = models.ForeignKey(Format, related_name="streams")


class Field(models.Model):
    name = models.CharField(max_length=100, validators=[no_spaces_validator, no_reserved_names_validator])
    type = models.CharField(choices=registry.get_choices("type"), max_length=255)
    source_template = models.CharField(max_length=255)
    format = models.ForeignKey(Format, related_name="fields")

    def get_field(self):
        return ExtractorField(
            name=self.name,
            source=FieldSource(self.source_template),
            transformers=[
                t.get_transformer() for t in self.transformations.all()
            ],
            type=self.get_field_type()
        )

    def get_field_type(self):
        return registry.get_by_name("type", self.type)

    def __unicode__(self):
        return "Field %s (%s) in %s" % (self.name, self.get_type_display(), self.format.name)


class Transform(models.Model):
    type = models.CharField(choices=registry.get_choices("transformer"), max_length=255)
    args = models.CharField(max_length=255, blank=True)
    field = models.ForeignKey(Field, related_name="transformations")

    class Meta:
        ordering = ("id",)

    def get_transformer(self):
        return registry.get_by_name("transformer", self.type)(self.args)