from django.db import models
from logstore.extractor.base import Format as ExtractorFormat, Field as ExtractorField, FieldSource
from logstore.extractor.register import registry
from django.core.exceptions import ValidationError
import string


def no_spaces(value):
    for char in string.whitespace:
        if char in value:
            raise ValidationError("Must not contain whitespace")


class Format(models.Model):
    name = models.CharField(max_length=250)

    def create_format(self):
        return ExtractorFormat(
            splitter=self.splitter.get_splitter(),
            fields=[field.get_field() for field in self.fields.all()]
        )

    def get_file_name_query(self, postfix=""):
        names = self.streams.values_list("name")
        if not names:
            return ""
        return " OR ".join('(stream_name:"%s")' % name for name in names) + postfix


class FormatStream(models.Model):
    name = models.CharField(max_length=250)
    format = models.ForeignKey("formats.Format", related_name="streams")


class Splitter(models.Model):
    type = models.CharField(choices=registry.get_splitter_choices(), max_length=255)
    args = models.CharField(max_length=250, null=True, blank=True)
    format = models.OneToOneField("formats.Format")

    def get_splitter(self):
        return registry.get_splitter_by_name(self.type)(self.args)


class Field(models.Model):
    name = models.CharField(max_length=100, validators=[no_spaces])
    type = models.CharField(choices=registry.get_type_choices(), max_length=255)
    source_template = models.CharField(max_length=255)
    format = models.ForeignKey("formats.Format", related_name="fields")

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
        return registry.get_type_by_name(self.type)

    def __unicode__(self):
        return "Field %s (%s) in %s" % (self.name, self.get_type_display(), self.format.name)


class Transform(models.Model):
    type = models.CharField(choices=registry.get_transformer_choices(), max_length=255)
    args = models.CharField(max_length=250, blank=True)
    field = models.ForeignKey("formats.Field", related_name="transformations")

    class Meta:
        ordering = ("id",)

    def get_transformer(self):
        return registry.get_transformer_by_name(self.type)(self.args)