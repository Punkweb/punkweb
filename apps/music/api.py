from rest_framework import serializers, viewsets, permissions, mixins, views

from apps.music.models import (
    Artist,
    Album,
    Audio,
    ArtistEvent,
)


class ArtistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Artist
        fields = "__all__"


class AlbumSerializer(serializers.ModelSerializer):
    class Meta:
        model = Album
        fields = "__all__"


class AudioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Audio
        fields = "__all__"


class ArtistEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = ArtistEvent
        fields = "__all__"


class ArtistViewSet(
    mixins.RetrieveModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet
):
    queryset = Artist.objects.order_by("name")
    serializer_class = ArtistSerializer

    def get_queryset(self):
        qs = self.queryset
        return qs.all()


class AlbumViewSet(
    mixins.RetrieveModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet
):
    queryset = Album.objects.order_by("artist", "title", "-release_date")
    serializer_class = AlbumSerializer

    def get_queryset(self):
        qs = self.queryset
        return qs.all()


class AudioViewSet(
    mixins.RetrieveModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet
):
    queryset = Audio.objects.order_by(
        "disc_num",
        "track_num",
        "title",
    )
    serializer_class = AudioSerializer

    def get_queryset(self):
        qs = self.queryset
        return qs.all()


class ArtistEventViewSet(
    mixins.RetrieveModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet
):
    queryset = ArtistEvent.objects.order_by("-event_date")
    serializer_class = ArtistEventSerializer

    def get_queryset(self):
        qs = self.queryset
        return qs.all()
