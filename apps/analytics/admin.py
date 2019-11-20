from django.contrib import admin
from . import models


class AnalyticsEventAdmin(admin.ModelAdmin):
    list_display = ("category", "action", "label", "occurred_at", )


class ClientErrorAdmin(admin.ModelAdmin):
    list_display = ("occurred_at", )


admin.site.register(models.AnalyticsEvent, AnalyticsEventAdmin)
