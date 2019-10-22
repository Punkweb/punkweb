from django.db import models
from django.contrib.postgres.fields import JSONField

from punkweb.mixins import (
    UUIDPrimaryKey,
    OccurredAtMixin,
)


class AnalyticsEvent(UUIDPrimaryKey, OccurredAtMixin):
    category = models.CharField(max_length=256, null=False, blank=False)
    action = models.CharField(max_length=256, null=False, blank=False)
    label = models.CharField(max_length=256, null=False, blank=False)
    metadata = JSONField(null=True, blank=True)

    class Meta:
        ordering = ("-occurred_at", )

    def __str__(self):
        return "{}: {}: {}".format(self.category, self.action, self.label)
