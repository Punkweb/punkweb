from django.contrib import admin

from apps.contact.models import ContactForm


class ContactFormAdmin(admin.ModelAdmin):
    list_display = (
        "contact_info",
        "created",
    )


admin.site.register(ContactForm, ContactFormAdmin)
