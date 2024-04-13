from easy_thumbnails.files import get_thumbnailer
from mutagen.mp3 import MP3
from rest_framework import serializers

from apps.music.models import Album, Artist, ArtistEvent, Audio


class ArtistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Artist
        fields = "__all__"
        lookup_field = "slug"

    def to_representation(self, instance):
        data = super().to_representation(instance)
        request = self.context.get("request")

        if instance.image:
            data["thumbnail"] = request.build_absolute_uri(
                get_thumbnailer(instance.image)["medium"].url
            )

        return data


class AlbumSerializer(serializers.ModelSerializer):
    class Meta:
        model = Album
        fields = "__all__"
        lookup_field = "slug"

    def to_representation(self, instance):
        data = super().to_representation(instance)
        request = self.context.get("request")

        if instance.cover_art:
            data["thumbnail"] = request.build_absolute_uri(
                get_thumbnailer(instance.cover_art)["medium"].url
            )

        if instance.artist:
            data["artist"] = ArtistSerializer(
                instance.artist,
                context={"request": request},
            ).data

        return data


class AudioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Audio
        fields = "__all__"

    def to_representation(self, instance):
        data = super().to_representation(instance)
        request = self.context.get("request")

        data["total_plays"] = instance.total_plays

        if instance.album:
            data["album"] = AlbumSerializer(
                instance.album,
                context={"request": request},
            ).data

        if instance.file.url.endswith(".mp3"):
            mp3_audio = MP3(instance.file)
            data["duration"] = mp3_audio.info.length
        else:
            data["duration"] = 0

        return data


class ArtistEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = ArtistEvent
        fields = "__all__"
        lookup_field = "slug"

    def to_representation(self, instance):
        data = super().to_representation(instance)
        request = self.context.get("request")

        if instance.event_image:
            data["thumbnail"] = request.build_absolute_uri(
                get_thumbnailer(instance.event_image)["medium"].url
            )

        if instance.artist:
            data["artist"] = ArtistSerializer(
                instance.artist,
                context={"request": request},
            ).data

        return data
