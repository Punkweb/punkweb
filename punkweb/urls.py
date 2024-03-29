"""punkweb URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls import url, include
from django.contrib import admin
from django.contrib.staticfiles.urls import static, staticfiles_urlpatterns
from django.views.generic.base import RedirectView
from rest_framework.routers import DefaultRouter

from punkweb import settings
from punkweb import views

app_name = "punkweb"

urlpatterns = [
    url(
        "favicon.ico",
        RedirectView.as_view(url=settings.STATIC_URL + "punkweb/favicon.ico"),
    ),
    url(r"^admin/", admin.site.urls),
    url(r"^board/", include("punkweb_boards.urls")),
    url(r"^api/", include("punkweb.rest.urls")),
    url(r"^$", views.index_view, name="index"),
]

urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
