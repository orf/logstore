from django.db import models
from .choices import SplitterChoice, TypeChoice, TransformChoice
from logstore.extractor.base import Format as ExtractorFormat, Field as ExtractorField, FieldSource
from logstore.extractor.splitters import Character, Shlex, Regex, DoNothing
from logstore.extractor.transformers import StripTransformer
import dbarray


class Format(models.Model):
    name = models.CharField(max_length=250)
    files = dbarray.CharArrayField(max_length=100)

    def create_format(self):
        return ExtractorFormat(
            splitter=self.splitter.get_splitter(),
            fields=[field.get_field() for field in self.fields.all()]
        )


class Splitter(models.Model):
    type = models.IntegerField(choices=SplitterChoice, default=SplitterChoice.CHARACTER)
    args = models.CharField(max_length=250, null=True, blank=True)
    format = models.OneToOneField("formats.Format")

    def get_splitter(self):
        return {SplitterChoice.CHARACTER: Character,
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
            ]
        )


class Transform(models.Model):
    type = models.IntegerField(choices=TransformChoice)
    args = models.CharField(max_length=250)
    field = models.ForeignKey("formats.Field", related_name="transformations")

    def get_transformer(self):
        return {TransformChoice.STRIP: StripTransformer}[self.type](self.args)