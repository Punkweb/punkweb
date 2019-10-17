from django.shortcuts import render, redirect, reverse


def index_view(request):
    return render(request, "punkweb/index.html", {})
