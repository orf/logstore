from django.db import models
from django.shortcuts import resolve_url


class Server(models.Model):
    name = models.CharField(max_length=255, unique=True)
    ip = models.IPAddressField(unique=True)
    suspended = models.BooleanField(default=False)

    def get_absolute_url(self):
        return resolve_url("servers:view", self.id)

    def get_search_query(self):
        return "server.id:%s" % self.id

    def get_last_messages_url(self):
        return "%s?server=%s" % (resolve_url("api:get_last_messages"), self.id)

    def __unicode__(self):
        return u"%s (%s)" % (self.name, self.ip)