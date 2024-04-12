import datetime

from django.db.models import Count
from django.db.models.functions import TruncDate
from easy_thumbnails.files import get_thumbnailer
from mutagen.mp3 import MP3
from rest_framework import serializers

from apps.analytics.models import AnalyticsEvent
from apps.music.models import Album, Artist, ArtistEvent, Audio
from apps.music.utils import listed_audio


class ArtistSerializer(serializers.ModelSerializer):
    thumbnail = serializers.SerializerMethodField()

    class Meta:
        model = Artist
        fields = "__all__"
        lookup_field = "slug"

    def get_thumbnail(self, obj):
        request = self.context.get("request")
        return request.build_absolute_uri(get_thumbnailer(obj.image)["medium"].url)


class AlbumSerializer(serializers.ModelSerializer):
    artist_slug = serializers.SerializerMethodField()
    artist_name = serializers.SerializerMethodField()
    thumbnail = serializers.SerializerMethodField()

    class Meta:
        model = Album
        fields = "__all__"
        lookup_field = "slug"

    def get_artist_slug(self, obj):
        return obj.artist.slug

    def get_artist_name(self, obj):
        return obj.artist.name

    def get_thumbnail(self, obj):
        request = self.context.get("request")
        return request.build_absolute_uri(get_thumbnailer(obj.cover_art)["medium"].url)


class AudioSerializer(serializers.ModelSerializer):
    artist_name = serializers.SerializerMethodField()
    artist_slug = serializers.SerializerMethodField()
    album_slug = serializers.SerializerMethodField()
    album_release_date = serializers.SerializerMethodField()
    album_thumbnail = serializers.SerializerMethodField()
    album_thumbnail_lrg = serializers.SerializerMethodField()
    duration = serializers.SerializerMethodField()
    total_plays = serializers.ReadOnlyField()

    class Meta:
        model = Audio
        fields = "__all__"

    def get_artist_name(self, obj):
        return obj.album.artist.name

    def get_artist_slug(self, obj):
        return obj.album.artist.slug

    def get_album_slug(self, obj):
        return obj.album.slug

    def get_album_release_date(self, obj):
        return obj.album.release_date

    def get_album_thumbnail(self, obj):
        request = self.context.get("request")
        return request.build_absolute_uri(
            get_thumbnailer(obj.album.cover_art)["medium"].url
        )

    def get_album_thumbnail_lrg(self, obj):
        request = self.context.get("request")
        return request.build_absolute_uri(
            get_thumbnailer(obj.album.cover_art)["large"].url
        )

    def get_duration(self, obj):
        if obj.file.url.endswith(".mp3"):
            mp3Audio = MP3(obj.file)
            return mp3Audio.info.length
        else:
            return 0


class ArtistEventSerializer(serializers.ModelSerializer):
    thumbnail = serializers.SerializerMethodField()
    artist_name = serializers.SerializerMethodField()
    artist_slug = serializers.SerializerMethodField()

    class Meta:
        model = ArtistEvent
        fields = "__all__"
        lookup_field = "slug"

    def get_thumbnail(self, obj):
        if not obj.event_image:
            return None
        request = self.context.get("request")
        return request.build_absolute_uri(
            get_thumbnailer(obj.event_image)["medium"].url
        )

    def get_artist_name(self, obj):
        return obj.artist.name

    def get_artist_slug(self, obj):
        return obj.artist.slug
