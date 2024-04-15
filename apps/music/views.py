from django.core.cache import cache
from rest_framework import mixins, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from apps.music.models import Album, Artist, ArtistEvent, Audio
from apps.music.serializers import (
    AlbumSerializer,
    ArtistEventSerializer,
    ArtistSerializer,
    AudioSerializer,
)
from apps.music.utils import listed_albums, listed_artists, listed_audio


class ArtistViewSet(
    mixins.RetrieveModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet
):
    queryset = Artist.objects.none()
    serializer_class = ArtistSerializer
    lookup_field = "slug"

    def get_queryset(self):
        qs = listed_artists(self.request)
        return qs.order_by("name")

    @action(detail=True, methods=["get"])
    def top_10(self, request, *args, **kwargs):
        artist_songs = listed_audio(request).filter(album__artist=self.get_object())
        all_song_ids = [song.id for song in artist_songs]
        songs = Audio.objects.filter(id__in=all_song_ids)
        sorted_songs = sorted(songs, key=lambda song: song.total_plays, reverse=True)
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
        qs = listed_albums(self.request)
        artist_id = self.request.query_params.get("artist_id")
        if artist_id:
            qs = qs.filter(artist__id=artist_id)
        return qs.order_by("artist", "-release_date", "title")


class AudioViewSet(
    mixins.RetrieveModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet
):
    queryset = Audio.objects.none()
    serializer_class = AudioSerializer

    def get_queryset(self):
        qs = listed_audio(self.request)
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
