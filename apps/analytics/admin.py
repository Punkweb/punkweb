from django.contrib import admin

from apps.analytics.models import AnalyticsEvent, ClientError


class AnalyticsEventAdmin(admin.ModelAdmin):
    list_display = (
        "category",
        "action",
        "label",
        "occurred_at",
    )


class ClientErrorAdmin(admin.ModelAdmin):
    list_display = ("occurred_at",)


admin.site.register(AnalyticsEvent, AnalyticsEventAdmin)
admin.site.register(ClientError, ClientErrorAdmin)
