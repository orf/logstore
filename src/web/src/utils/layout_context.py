from apps.managers.servers.models import Server


def layout_context(request):
    return {"servers": Server.objects.all()}