from django.shortcuts import render, redirect, reverse


def index_view(request):
    return render(request, 'punkweb/index.html', {})


def links_view(request):
    return render(request, 'punkweb/links.html', {})


def pgp_view(request):
    return render(request, 'punkweb/pgp.html', {})
