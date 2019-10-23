from django.contrib import admin
from . import models


class ContactFormAdmin(admin.ModelAdmin):
    list_display = ("contact_info", "created",)


admin.site.register(models.ContactForm, ContactFormAdmin)
