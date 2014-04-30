from django.conf import settings
from django.contrib.auth.views import login
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse


IGNORED_PATHS = [reverse("login"), reverse("api:server_auth")]


class RequireLoginMiddleware(object):
    """
    Require Login middleware. If enabled, each Django-powered page will
    require authentication.
    
    If an anonymous user requests a page, he/she is redirected to the login
    page set by REQUIRE_LOGIN_PATH or /accounts/login/ by default.
    """
    def __init__(self):
        self.require_login_path = reverse("login")
    
    def process_request(self, request):
        if request.path not in IGNORED_PATHS and request.user.is_anonymous():
            if request.POST:
                return login(request)
            else:
                return HttpResponseRedirect('%s?next=%s' % (self.require_login_path, request.path))