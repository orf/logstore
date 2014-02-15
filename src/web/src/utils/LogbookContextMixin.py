

class PageMixin(object):
    PAGE_TITLE = ""

    def get_context_data(self, **kwargs):
        ctx = super(PageMixin, self).get_context_data(**kwargs)
        ctx.update({"page_title": self.PAGE_TITLE})
        return ctx