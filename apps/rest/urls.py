from django.conf.urls import url, include
from rest_framework import routers

from apps.rest import api


router = routers.DefaultRouter()
router.register(r"artists", api.ArtistViewSet, base_name="artists")
router.register(r"albums", api.AlbumViewSet, base_name="albums")
router.register(r"audio", api.AudioViewSet, base_name="audio")
router.register(r"artist_events", api.ArtistEventViewSet, base_name="artist_events")
router.register(r"users", api.UserViewSet)

app_name = "rest"

urlpatterns = [
    url(r"^", include(router.urls)),
    url(r"^auth/", include("rest_framework.urls", namespace="rest_framework")),
    url(r"^token-auth/", api.obtain_auth_token),
]
