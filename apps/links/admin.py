from django.contrib import admin
from apps.links.models import Category, Link


class CategoryAdmin(admin.ModelAdmin):
    pass


class LinkAdmin(admin.ModelAdmin):
    pass


admin.site.register(Category, CategoryAdmin)
admin.site.register(Link, LinkAdmin)
