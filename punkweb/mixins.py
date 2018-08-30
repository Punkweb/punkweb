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


class UUIDPrimaryKey(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    class Meta:
        abstract = True
