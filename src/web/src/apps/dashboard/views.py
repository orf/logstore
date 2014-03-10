from django.views.generic import TemplateView

from ..statistics.models import get_latest_snapshot


# Create your views here.
class Dashboard(TemplateView):
    PAGE_TITLE = "Dashboard"

    def get_context_data(self, **kwargs):
        ctx = super(Dashboard, self).get_context_data(**kwargs)
        ctx.update({"page_title": self.PAGE_TITLE,
                    "stats": get_latest_snapshot()})
        return ctx