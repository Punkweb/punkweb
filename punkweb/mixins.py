import uuid
from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import models
from easy_thumbnails.files import get_thumbnailer
from punkweb_boards import utils


class CreatedModifiedMixin(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class UploadedAtMixin(models.Model):
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True


class OccurredAtMixin(models.Model):
    occurred_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True


class UUIDPrimaryKey(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    class Meta:
        abstract = True


class AddressMixin(models.Model):
    address_line = models.CharField(max_length=256, null=True, blank=True)
    zip_code = models.CharField(max_length=256, null=True, blank=True)
    city = models.CharField(max_length=256, null=True, blank=True)
    state = models.CharField(max_length=256, null=True, blank=True)
    country = models.CharField(max_length=256, null=True, blank=True)

    @property
    def full_address(self):
        return '{}, {}, {} {}'.format(
            self.address_line, self.city, self.state, self.zip_code)

    class Meta:
        abstract = True
