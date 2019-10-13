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
from django.conf.urls import url, include
from django.contrib import admin
from django.contrib.staticfiles.urls import static, staticfiles_urlpatterns
from rest_framework.routers import DefaultRouter

from punkweb import settings
from punkweb import views
from apps.music import api as music_api

app_name = "punkweb"

router = DefaultRouter()
router.register(r'artists', music_api.ArtistViewSet, base_name='artists')
router.register(r'albums', music_api.AlbumViewSet, base_name='albums')
router.register(r'audio', music_api.AudioViewSet, base_name='audio')
router.register(r'artist_events', music_api.ArtistEventViewSet, base_name='artist_events')

urlpatterns = [
    # Package urls
    url(r"^admin/", admin.site.urls),
    url(r"^board/", include("punkweb_boards.urls")),
    url(r"^board/page/", include("punkweb_boards.page_urls")),
    url(r"^board/api/", include("punkweb_boards.rest.urls")),
    url(r"^captcha/", include("captcha.urls")),
    # Site urls
    url(r'^api/', include(router.urls)),
    url(r"^$", views.index_view, name="index"),
    url(r"^music/", include("apps.music.urls")),
    url(r"^game/$", views.shietyshooter_view, name="game"),
    url(r"^shietyshooter/$", views.shietyshooter_view, name="shietyshooter"),
    url(r"^diablo/$", views.diablo_view, name="diablo"),
]

urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
