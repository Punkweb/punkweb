import datetime
from rest_framework import viewsets, permissions, mixins, views
from rest_framework.decorators import action
from rest_framework.response import Response

from apps.contact.models import (
    ContactForm,
)

from apps.contact.serializers import (
    ContactFormSerializer,
)


class ContactFormViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    queryset = ContactForm.objects.all()
    serializer_class = ContactFormSerializer

    def get_queryset(self):
        qs = self.queryset
        return qs.order_by("-created")
