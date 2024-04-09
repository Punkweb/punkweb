from django.db import models

from punkweb.mixins import CreatedModifiedMixin, UUIDPrimaryKey


class ContactForm(UUIDPrimaryKey, CreatedModifiedMixin):
    contact_info = models.CharField(max_length=256, null=False, blank=False)
    subject = models.CharField(max_length=256, null=False, blank=False)
    body = models.TextField(max_length=2000, null=False, blank=False)

    class Meta:
        ordering = ("-created",)

    def __str__(self):
        return "{}: {}".format(self.contact_info, self.subject)
