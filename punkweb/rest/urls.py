from apps.analytics.views import AnalyticsEventViewSet, ClientErrorViewSet
from apps.contact.views import ContactFormViewSet
from apps.music.views import (
    AlbumViewSet,
    ArtistEventViewSet,
    ArtistViewSet,
    AudioViewSet,
)
from django.urls import include, path
from punkweb.rest.views import UserCreateView, UserViewSet, obtain_auth_token
from rest_framework import routers

router = routers.DefaultRouter()

router.register(r"analytics/analytics_events", AnalyticsEventViewSet)
router.register(r"analytics/client_errors", ClientErrorViewSet)
router.register(r"contact_forms", ContactFormViewSet)
router.register(r"artists", ArtistViewSet)
router.register(r"albums", AlbumViewSet)
router.register(r"audio", AudioViewSet)
router.register(r"artist_events", ArtistEventViewSet)
router.register(r"users", UserViewSet)

urlpatterns = [
    path("", include(router.urls)),
    path("auth/", include("rest_framework.urls", namespace="rest_framework")),
    path("token-auth/", obtain_auth_token),
    path("register/", UserCreateView.as_view(), name="create-account"),
]
