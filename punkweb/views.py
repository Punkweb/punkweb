from django.shortcuts import render, redirect, reverse


def index_view(request):
    return render(request, "punkweb/index.html", {})


def shietyshooter_view(request):
    return render(request, "punkweb/shietyshooter.html", {})


def diablo_view(request):
    return render(request, "punkweb/diablo.html", {})
