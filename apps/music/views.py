import datetime
from django.db.models.functions import TruncDate
from django.db.models import Count
from rest_framework import viewsets, permissions, mixins, views
from rest_framework.decorators import action
from rest_framework.response import Response

from apps.analytics.models import (
    AnalyticsEvent,
)
from apps.analytics.serializers import (
    AnalyticsEventSerializer,
)

from apps.music.models import (
    Artist,
    Album,
    Audio,
    ArtistEvent,
)

from apps.music.serializers import (
    ArtistSerializer,
    AlbumSerializer,
    AudioSerializer,
    ArtistEventSerializer,
)

from punkweb.rest import utils as rest_utils


class ArtistViewSet(
    mixins.RetrieveModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet
):
    queryset = Artist.objects.none()
    serializer_class = ArtistSerializer
    lookup_field = "slug"

    def get_queryset(self):
        qs = rest_utils.listed_artists(self.request)
        return qs.order_by("name")

    @action(detail=True, methods=["get"])
    def top_10(self, request, *args, **kwargs):
        artist_songs = rest_utils.listed_audio(request).filter(
            album__artist__id=self.get_object().id
        )
        all_song_ids = [
            song.id for song in artist_songs if song.total_plays > 0
        ]
        songs = Audio.objects.filter(id__in=all_song_ids)
        sorted_songs = sorted(
            songs, key=lambda song: song.total_plays, reverse=True
        )
        serializer = AudioSerializer(
            sorted_songs[:10], many=True, context={"request": request}
        )
        return Response(serializer.data, status=200)


class AlbumViewSet(
    mixins.RetrieveModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet
):
    queryset = Album.objects.none()
    serializer_class = AlbumSerializer
    lookup_field = "slug"

    def get_serializer_context(self):
        context = super(AlbumViewSet, self).get_serializer_context()
        return context

    def get_queryset(self):
        qs = rest_utils.listed_albums(self.request)
        artist_id = self.request.query_params.get("artist_id")
        if artist_id:
            qs = qs.filter(artist__id=artist_id)
        return qs.order_by("artist", "-release_date", "title")

    @action(detail=False, methods=["get"])
    def latest_releases(self, request):
        qs = self.get_queryset().order_by("-release_date")[:5]
        serializer = self.get_serializer(qs.all(), many=True)
        return Response(serializer.data)


class AudioViewSet(
    mixins.RetrieveModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet
):
    queryset = Audio.objects.none()
    serializer_class = AudioSerializer

    def get_queryset(self):
        qs = rest_utils.listed_audio(self.request)
        artist_id = self.request.query_params.get("artist_id")
        if artist_id:
            qs = qs.filter(album__artist__id=artist_id)
        album_id = self.request.query_params.get("album_id")
        if album_id:
            qs = qs.filter(album__id=album_id)
        return qs.order_by(
            "disc_num",
            "track_num",
            "title",
        )


class ArtistEventViewSet(
    mixins.RetrieveModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet
):
    queryset = ArtistEvent.objects.order_by("-event_date")
    serializer_class = ArtistEventSerializer
    lookup_field = "slug"

    def get_queryset(self):
        qs = self.queryset
        artist_id = self.request.query_params.get("artist_id")
        if artist_id:
            qs = qs.filter(artist__id=artist_id)
        return qs.all()

    @action(detail=False, methods=["get"])
    def this_week(self, request):
        qs = self.get_queryset()
        today_beginning = datetime.datetime.combine(
            datetime.date.today(), datetime.time()
        )
        one_week_from_now = today_beginning + datetime.timedelta(days=7)
        qs = qs.filter(
            event_date__gte=today_beginning, event_date__lte=one_week_from_now
        )
        serializer = self.get_serializer(qs.all(), many=True)
        return Response(serializer.data)
