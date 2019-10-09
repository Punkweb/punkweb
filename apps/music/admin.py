from django.contrib import admin
from . import models


class ArtistAdmin(admin.ModelAdmin):
    list_display = ('name', 'genre', 'is_listed',)


class AlbumAdmin(admin.ModelAdmin):
    list_display = ('title', 'year', 'genre', 'is_listed',)


class MusicAdmin(admin.ModelAdmin):
    list_display = ('title', 'album', 'disc_num', 'track_num',)


admin.site.register(models.Artist, ArtistAdmin)
admin.site.register(models.Album, AlbumAdmin)
admin.site.register(models.Audio, MusicAdmin)
