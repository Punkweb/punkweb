from django.shortcuts import render, redirect

from apps.music import models


def index_view(request):
    artists = models.Artist.objects.all()
    albums = models.Album.objects.all()
    audio = models.Audio.objects.all()
    compilations = models.AudioCompilation.objects.all()
    context = {
        'artists': artists,
        'albums': albums,
        'audio': audio,
        'compilations': compilations
    }
    return render(request, 'music/index.html', context)


def audio_view(request, slug):
    song = models.Audio.objects.get(slug=slug)
    context = {
        'song': song
    }
    return render(request, 'music/audio_view.html', context)


def artist_view(request, slug):
    artist = models.Artist.objects.get(slug=slug)
    albums = models.Album.objects.filter(artist=artist)
    songs = models.Audio.objects.filter(album__artist=artist)
    featured_on_compilations = models.AudioCompilation.objects.filter(
        tracks__id__in=songs).distinct()
    context = {
        'artist': artist,
        'albums': albums,
        'featured_on_compilations': featured_on_compilations,
    }
    return render(request, 'music/artist.html', context)


def album_view(request, slug):
    album = models.Album.objects.get(slug=slug)
    songs = models.Audio.objects.filter(album=album)
    context = {
        'album': album,
        'songs': songs,
    }
    return render(request, 'music/album.html', context)


def audio_compilation_view(request, slug):
    compilation = models.AudioCompilation.objects.get(slug=slug)
    tracks = compilation.tracks
    context = {
        'compilation': compilation,
        'tracks': tracks
    }
    return render(request, 'music/audio_compilation_view.html', context)
