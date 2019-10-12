import datetime
from django.shortcuts import render, redirect

from apps.music import models


def listed_artists(request):
    objects = models.Artist.objects

    if request.user and request.user.is_superuser:
        return objects.filter(
            albums__isnull=False
        ).distinct().order_by("name")

    listed = objects.filter(
        is_listed=True,
        albums__isnull=False,
    ).distinct()
    return listed.order_by("name")


def listed_albums(request):
    objects = models.Album.objects

    if request.user and request.user.is_superuser:
        return objects.filter(
            tracks__isnull=False
        ).distinct().order_by("-release_date")

    listed = objects.filter(
        is_listed=True,
        tracks__isnull=False,
    ).distinct()
    return listed.order_by("-release_date")


def listed_audio(request):
    objects = models.Audio.objects

    if request.user and request.user.is_superuser:
        return objects.all().order_by("disc_num", "track_num")

    return objects.filter(album__is_listed=True).order_by(
        "disc_num", "track_num"
    )


def index_view(request):
    artists = listed_artists(request)
    albums = listed_albums(request)
    audio = listed_audio(request)

    today_beginning = datetime.datetime.combine(datetime.date.today(), datetime.time())
    one_week_from_now = today_beginning + datetime.timedelta(days=7)
    events_this_week = models.ArtistEvent.objects.filter(
        event_date__gte=today_beginning, event_date__lte=one_week_from_now)

    context = {
        "artists": artists,
        "albums": albums,
        "audio": audio,
        "latest_releases": albums.order_by("-release_date")[:5],
        "events_this_week": events_this_week,
    }
    return render(request, "music/index.html", context)


def artist_view(request, slug):
    artist = listed_artists(request).get(slug=slug)
    albums = listed_albums(request).filter(artist=artist)
    latest_release = albums.order_by('-release_date').first()

    today_beginning = datetime.datetime.combine(
        datetime.date.today(), datetime.time())
    events = artist.events.all()

    past_events = events.filter(event_date__lte=today_beginning)
    upcoming_events = events.filter(event_date__gte=today_beginning)
    context = {
        "artist": artist,
        "albums": albums,
        "latest_release": latest_release,
        "past_events": past_events,
        "upcoming_events": upcoming_events,
    }
    return render(request, "music/artist.html", context)


def album_view(request, slug):
    album = listed_albums(request).get(slug=slug)
    songs = listed_audio(request).filter(album=album)
    context = {"album": album, "songs": songs}
    return render(request, "music/album.html", context)


def audio_view(request, slug):
    song = listed_audio(request).get(slug=slug)
    context = {"song": song}
    return render(request, "music/audio_view.html", context)
