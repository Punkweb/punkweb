from django.contrib import admin
from . import models


class AnalyticsEventAdmin(admin.ModelAdmin):
    list_display = ("category", "action", "label", )


admin.site.register(models.AnalyticsEvent, AnalyticsEventAdmin)
