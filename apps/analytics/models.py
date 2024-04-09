from django.db import models
from punkweb.mixins import OccurredAtMixin, UUIDPrimaryKey


class AnalyticsEvent(UUIDPrimaryKey, OccurredAtMixin):
    category = models.CharField(max_length=256, null=False, blank=False)
    action = models.CharField(max_length=256, null=False, blank=False)
    label = models.CharField(max_length=256, null=False, blank=False)
    metadata = models.JSONField(null=True, blank=True)

    class Meta:
        ordering = ("-occurred_at",)

    def __str__(self):
        return "{}: {}: {}".format(self.category, self.action, self.label)


class ClientError(UUIDPrimaryKey, OccurredAtMixin):
    error_body = models.TextField(max_length=2048, null=False, blank=False)

    class Meta:
        ordering = ("-occurred_at",)

    def __str__(self):
        return "Client Error at {}".format(self.occurred_at)
