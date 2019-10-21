from rest_framework import serializers

from apps.analytics.models import (
    AnalyticsEvent,
)


class AnalyticsEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = AnalyticsEvent
        fields = "__all__"
