from django.db import models
from .choices import SplitterChoice, TypeChoice, TransformChoice
import dbarray


class Format(models.Model):
    name = models.CharField(max_length=250)
    files = dbarray.CharArrayField(max_length=100)


class Splitter(models.Model):
    type = models.IntegerField(choices=SplitterChoice, default=SplitterChoice.CHARACTER)
    args = models.CharField(max_length=250, null=True, blank=True)
    format = models.OneToOneField("formats.Format")


class Field(models.Model):
    name = models.CharField(max_length=100)
    type = models.IntegerField(choices=TypeChoice, default=TypeChoice.INTEGER)
    source_index = models.CharField(max_length=255)
    format = models.ForeignKey("formats.Format", related_name="fields")


class Transform(models.Model):
    type = models.IntegerField(choices=TransformChoice)
    args = models.CharField(max_length=250)
    field = models.ForeignKey("formats.Field", related_name="transformations")