from django.shortcuts import render, redirect

from apps.music import models


def listed_artists(request):
    objects = models.Artist.objects
    if request.user and request.user.is_superuser:
        return objects.all().order_by('name')
    return objects.filter(is_listed=True).order_by('name')


def listed_albums(request):
    objects = models.Album.objects
    if request.user and request.user.is_superuser:
        return objects.all().order_by('-year')
    return objects.filter(is_listed=True).order_by('-year')


def listed_audio(request):
    objects = models.Audio.objects
    if request.user and request.user.is_superuser:
        return objects.all().order_by('disc_num', 'track_num')
    return objects.filter(album__is_listed=True).order_by('disc_num', 'track_num')


def index_view(request):
    artists = listed_artists(request)
    albums = listed_albums(request)
    audio = listed_audio(request)
    context = {
        'artists': artists,
        'albums': albums,
        'audio': audio,
    }
    return render(request, 'music/index.html', context)


def audio_view(request, slug):
    song = listed_audio(request).get(slug=slug)
    context = {
        'song': song
    }
    return render(request, 'music/audio_view.html', context)


def artist_view(request, slug):
    artist = listed_artists(request).get(slug=slug)
    albums = listed_albums(request).filter(artist=artist)
    songs = listed_audio(request).filter(album__artist=artist)
    context = {
        'artist': artist,
        'albums': albums,
    }
    return render(request, 'music/artist.html', context)


def album_view(request, slug):
    album = listed_albums(request).get(slug=slug)
    songs = listed_audio(request).filter(album=album)
    context = {
        'album': album,
        'songs': songs,
    }
    return render(request, 'music/album.html', context)
