from django.shortcuts import render, redirect, reverse
from apps.links.models import Category, Link


def links_view(request):
    categories = Category.objects.all()
    context = {'categories': categories}
    return render(request, 'punkweb/links.html', context)
