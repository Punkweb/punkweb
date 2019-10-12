from django.contrib import admin
from . import models


class ArtistAdmin(admin.ModelAdmin):
    list_display = ("name", "genre", "is_listed")


class AlbumAdmin(admin.ModelAdmin):
    list_display = ("title", "artist", "release_date", "is_listed")


class AudioAdmin(admin.ModelAdmin):
    list_display = ("title", "album", "disc_num", "track_num")


class ArtistEventAdmin(admin.ModelAdmin):
    list_display = ("artist", "venue", "event_date")


admin.site.register(models.Artist, ArtistAdmin)
admin.site.register(models.Album, AlbumAdmin)
admin.site.register(models.Audio, AudioAdmin)
admin.site.register(models.ArtistEvent, ArtistEventAdmin)
