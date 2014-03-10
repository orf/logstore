from django.db import models
from logstore.extractor.base import Format as ExtractorFormat, Field as ExtractorField, FieldSource
from logstore.extractor.splitters import Character, Shlex, Regex, DoNothing, Space
from logstore.extractor.transformers import RemoveTransformer

from ..analyser.extractor_additions.transformers import GeoIPLookup
from .choices import SplitterChoice, TypeChoice, TransformChoice


class Format(models.Model):
    name = models.CharField(max_length=250)

    def create_format(self):
        return ExtractorFormat(
            splitter=self.splitter.get_splitter(),
            fields=[field.get_field() for field in self.fields.all()]
        )


class FormatFile(models.Model):
    name = models.CharField(max_length=250)
    format = models.ForeignKey("formats.Format", related_name="files")


class Splitter(models.Model):
    type = models.IntegerField(choices=SplitterChoice, default=SplitterChoice.CHARACTER)
    args = models.CharField(max_length=250, null=True, blank=True)
    format = models.OneToOneField("formats.Format")

    def get_splitter(self):
        return {SplitterChoice.CHARACTER: Character,
                SplitterChoice.SPACE: Space,
                SplitterChoice.NONE: DoNothing,
                SplitterChoice.REGEX: Regex,
                SplitterChoice.SHLEX: Shlex}[self.type](self.args)


class Field(models.Model):
    name = models.CharField(max_length=100)
    type = models.IntegerField(choices=TypeChoice, default=TypeChoice.INTEGER)
    source_index = models.CharField(max_length=255)
    format = models.ForeignKey("formats.Format", related_name="fields")

    def get_field(self):
        return ExtractorField(
            name=self.name,
            source=FieldSource(self.source_index),
            transformers=[
                t.get_transformer() for t in self.transformations.all()
            ],
            type=self.get_field_type()
        )

    def get_field_type(self):
        return {TypeChoice.INTEGER: int,
                TypeChoice.DATETIME: None,
                TypeChoice.IP_ADDRESS: None}[self.type]


class Transform(models.Model):
    type = models.IntegerField(choices=TransformChoice)
    args = models.CharField(max_length=250, blank=True)
    field = models.ForeignKey("formats.Field", related_name="transformations")

    class Meta:
        ordering = ("id",)

    def get_transformer(self):
        return {TransformChoice.REMOVE: RemoveTransformer,
                TransformChoice.IP_LOOKUP: GeoIPLookup}[self.type](self.args)