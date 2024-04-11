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
    plays_this_week = serializers.SerializerMethodField()

    class Meta:
        model = Artist
        fields = "__all__"
        lookup_field = "slug"

    def get_thumbnail(self, obj):
        request = self.context.get("request")
        return request.build_absolute_uri(get_thumbnailer(obj.image)["medium"].url)

    def get_plays_this_week(self, obj):
        all_song_ids = (
            listed_audio(self.context.get("request"))
            .filter(album__artist__id=obj.id)
            .distinct()
            .values_list("id", flat=True)
        )
        all_song_ids = map(lambda x: str(x), all_song_ids.all())
        last_week = datetime.datetime.today() - datetime.timedelta(days=7)
        tomorrow = datetime.datetime.today() + datetime.timedelta(days=1)
        song_play_events = (
            AnalyticsEvent.objects.filter(
                action__iexact="30_second_song_play",
                metadata__isnull=False,
                metadata__song_id__isnull=False,
                metadata__song_id__in=all_song_ids,
                occurred_at__range=[
                    last_week.strftime("%Y-%m-%d"),
                    tomorrow.strftime("%Y-%m-%d"),
                ],
            )
            .annotate(date=TruncDate("occurred_at"))
            .values("date")
            .annotate(plays=Count("id"))
            .values("date", "plays")
            .order_by("-date")[:7]
        )
        return song_play_events


class AlbumSerializer(serializers.ModelSerializer):
    artist_slug = serializers.SerializerMethodField()
    artist_name = serializers.SerializerMethodField()
    thumbnail = serializers.SerializerMethodField()
    total_song_plays = serializers.SerializerMethodField()

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

    def get_total_song_plays(self, obj):
        all_song_ids = (
            listed_audio(self.context.get("request"))
            .filter(album__id=obj.id)
            .distinct()
            .values_list("id", flat=True)
        )
        all_song_ids = map(lambda x: str(x), all_song_ids.all())
        song_play_events = AnalyticsEvent.objects.filter(
            action__iexact="30_second_song_play",
            metadata__isnull=False,
            metadata__song_id__isnull=False,
            metadata__song_id__in=all_song_ids,
            metadata__user_is_staff=False,
        )
        return song_play_events.count()


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
