from django.contrib import admin
from apps.links.models import Category, Link


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'order')


class LinkAdmin(admin.ModelAdmin):
    list_display = ('display_text', 'category', 'active')


admin.site.register(Category, CategoryAdmin)
admin.site.register(Link, LinkAdmin)
