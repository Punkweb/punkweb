from django.db import models

from easy_thumbnails.fields import ThumbnailerImageField
from precise_bbcode.fields import BBCodeTextField

from punkweb.mixins import (
    UploadedAtMixin,
    CreatedModifiedMixin,
    UUIDPrimaryKey,
    AddressMixin,
)


def audio_upload_to(instance, filename):
    ext = (filename.split(".")[-1]).lower()
    filename = "{}.{}".format(instance.slug, ext)
    return "/".join(["music", "audio", filename])


def audio_compilation_upload_to(instance, filename):
    ext = (filename.split(".")[-1]).lower()
    filename = "{}.{}".format(instance.slug, ext)
    return "/".join(["music", "compilations", filename])


def artist_image_upload_to(instance, filename):
    ext = (filename.split(".")[-1]).lower()
    filename = "{}.{}".format(instance.slug, ext)
    return "/".join(["music", "artists", filename])


def album_cover_upload_to(instance, filename):
    ext = (filename.split(".")[-1]).lower()
    filename = "{}.{}".format(instance.slug, ext)
    return "/".join(["music", "album", filename])


def artist_event_upload_to(instance, filename):
    ext = (filename.split(".")[-1]).lower()
    filename = "{}.{}".format(instance.slug, ext)
    return "/".join(["music", "artist_events", filename])


class Artist(UUIDPrimaryKey):
    slug = models.SlugField(
        max_length=256, blank=False, null=False, unique=True
    )
    name = models.CharField(max_length=256, blank=False, null=False)
    genre = models.CharField(max_length=256)
    bio = BBCodeTextField(max_length=5096, blank=True, null=True)
    image = ThumbnailerImageField(
        upload_to=artist_image_upload_to, blank=True, null=True
    )
    is_listed = models.BooleanField(default=False)

    spreadshirt_shop_slug = models.SlugField(
        max_length=256, blank=True, null=True,
    )

    class Meta:
        ordering = ("name",)

    def __str__(self):
        return self.name


class Album(UUIDPrimaryKey):
    slug = models.SlugField(
        max_length=256, blank=False, null=False, unique=True
    )
    artist = models.ForeignKey(
        "Artist",
        blank=False,
        null=False,
        related_name="albums",
        on_delete=models.CASCADE,
    )
    title = models.CharField(max_length=256, blank=False, null=False)
    release_date = models.DateField()
    cover_art = ThumbnailerImageField(
        upload_to=album_cover_upload_to, blank=True, null=True
    )
    genre = models.CharField(max_length=256)
    is_listed = models.BooleanField(default=False)

    class Meta:
        ordering = ("artist", "title", "-release_date")

    def __str__(self):
        return "{}: {}".format(self.artist.name, self.title)


class TrackInformationMixin(models.Model):
    slug = models.SlugField(
        max_length=256, blank=False, null=False, unique=True
    )
    title = models.CharField(max_length=256, blank=False, null=False)
    album = models.ForeignKey(
        "Album",
        blank=True,
        null=True,
        related_name="tracks",
        on_delete=models.SET_NULL,
    )
    disc_num = models.IntegerField()
    track_num = models.IntegerField()
    bbcode_lyrics = BBCodeTextField(max_length=32768, blank=True, null=True)

    class Meta:
        abstract = True


class Audio(UUIDPrimaryKey, UploadedAtMixin, TrackInformationMixin):
    file = models.FileField(upload_to=audio_upload_to, blank=False, null=False)

    class Meta:
        ordering = (
            "album__artist__name",
            "album__title",
            "disc_num",
            "track_num",
            "title",
        )

    def __str__(self):
        return "{}".format(self.title)


class ArtistEvent(UUIDPrimaryKey, CreatedModifiedMixin, AddressMixin):
    slug = models.SlugField(
        max_length=256, blank=False, null=False, unique=True
    )
    title = models.CharField(max_length=256, blank=False, null=False)
    venue = models.CharField(max_length=256, blank=True, null=True)
    artist = models.ForeignKey(
        "Artist",
        blank=False,
        null=False,
        related_name="events",
        on_delete=models.CASCADE,
    )
    event_date = models.DateField(blank=False, null=False)
    event_image = models.ImageField(
        upload_to=artist_event_upload_to, blank=True, null=True
    )

    class Meta:
        ordering = ("-event_date", )

    def __str__(self):
        return "{} at {}, {}".format(self.artist.name, self.venue, self.city)
