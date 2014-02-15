from django.shortcuts import render
from django.views.generic import TemplateView
from utils.LogbookContextMixin import PageMixin


# Create your views here.
class Dashboard(PageMixin, TemplateView):
    PAGE_TITLE = "Dashboard"