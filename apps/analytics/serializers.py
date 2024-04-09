from rest_framework import serializers

from apps.analytics.models import AnalyticsEvent, ClientError


class AnalyticsEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = AnalyticsEvent
        fields = "__all__"


class ClientErrorSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClientError
        fields = "__all__"
