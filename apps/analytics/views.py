from rest_framework import mixins, viewsets

from apps.analytics.models import AnalyticsEvent, ClientError
from apps.analytics.serializers import AnalyticsEventSerializer, ClientErrorSerializer


class AnalyticsEventViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    queryset = AnalyticsEvent.objects.all()
    serializer_class = AnalyticsEventSerializer

    def get_queryset(self):
        qs = self.queryset
        return qs.order_by("-occurred_at")


class ClientErrorViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    queryset = ClientError.objects.all()
    serializer_class = ClientErrorSerializer

    def get_queryset(self):
        qs = self.queryset
        return qs.order_by("-occurred_at")
