from rest_framework import serializers
from easy_thumbnails.files import get_thumbnailer

from apps.analytics.models import (
    AnalyticsEvent,
)

from apps.music.models import (
    Artist,
    Album,
    Audio,
    ArtistEvent,
)


class ArtistSerializer(serializers.ModelSerializer):
    thumbnail = serializers.SerializerMethodField()

    class Meta:
        model = Artist
        fields = "__all__"
        lookup_field = 'slug'

    def get_thumbnail(self, obj):
        request = self.context.get('request')
        return request.build_absolute_uri(get_thumbnailer(obj.image)['avatar'].url)


class AlbumSerializer(serializers.ModelSerializer):
    artist_slug = serializers.SerializerMethodField()
    artist_name = serializers.SerializerMethodField()
    thumbnail = serializers.SerializerMethodField()

    class Meta:
        model = Album
        fields = "__all__"
        lookup_field = 'slug'

    def get_artist_slug(self, obj):
        return obj.artist.slug

    def get_artist_name(self, obj):
        return obj.artist.name

    def get_thumbnail(self, obj):
        request = self.context.get('request')
        return request.build_absolute_uri(get_thumbnailer(obj.cover_art)['avatar'].url)


class AudioSerializer(serializers.ModelSerializer):
    artist_name = serializers.SerializerMethodField()
    album_release_date = serializers.SerializerMethodField()
    album_thumbnail = serializers.SerializerMethodField()
    total_song_plays = serializers.SerializerMethodField()

    class Meta:
        model = Audio
        fields = "__all__"

    def get_artist_name(self, obj):
        return obj.album.artist.name

    def get_album_release_date(self, obj):
        return obj.album.release_date

    def get_album_thumbnail(self, obj):
        request = self.context.get('request')
        return request.build_absolute_uri(get_thumbnailer(obj.album.cover_art)['avatar'].url)

    def get_total_song_plays(self, obj):
        finished_song_events = AnalyticsEvent.objects.filter(
            action__iexact="finished_song",
            metadata__isnull=False,
            metadata__song_id__isnull=False,
            metadata__song_id=str(obj.id),
        )
        return finished_song_events.count()


class ArtistEventSerializer(serializers.ModelSerializer):
    thumbnail = serializers.SerializerMethodField()
    artist_name = serializers.SerializerMethodField()
    artist_slug = serializers.SerializerMethodField()

    class Meta:
        model = ArtistEvent
        fields = "__all__"
        lookup_field = 'slug'

    def get_thumbnail(self, obj):
        request = self.context.get('request')
        return request.build_absolute_uri(get_thumbnailer(obj.event_image)['avatar'].url)

    def get_artist_name(self, obj):
        return obj.artist.name

    def get_artist_slug(self, obj):
        return obj.artist.slug
