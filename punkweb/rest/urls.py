from django.conf.urls import url, include
from rest_framework import routers

from apps.analytics.views import (
    AnalyticsEventViewSet,
    ClientErrorViewSet,
)

from apps.contact.views import (
    ContactFormViewSet,
)

from apps.music.views import (
    ArtistViewSet,
    AlbumViewSet,
    AudioViewSet,
    ArtistEventViewSet,
)

from punkweb_boards.rest.views import (
    BoardProfileViewSet,
    CategoryViewSet,
    SubcategoryViewSet,
    ThreadViewSet,
    PostViewSet,
    ConversationViewSet,
    MessageViewSet,
    ShoutViewSet,
)

from punkweb.rest.views import (
    UserViewSet,
    UserCreateView,
    obtain_auth_token,
)

router = routers.DefaultRouter()

router.register(
    r"analytics/analytics_events", AnalyticsEventViewSet, basename="analytics_events")
router.register(
    r"analytics/client_errors", ClientErrorViewSet, basename="client_errors")
router.register(r"contact_forms", ContactFormViewSet, basename="contact_forms")

router.register(r"board/categories", CategoryViewSet, basename="categories")
router.register(r"board/subcategories", SubcategoryViewSet, basename="subcategories")
router.register(r"board/threads", ThreadViewSet, basename="threads")
router.register(r"board/posts", PostViewSet, basename="posts")
# router.register(r"board/conversations", ConversationViewSet, base_name="conversations")
# router.register(r"board/messages", MessageViewSet, base_name="messages")
router.register(r"board/shouts", ShoutViewSet, basename="shouts")
router.register(r"board/profiles", BoardProfileViewSet, basename="profiles")

router.register(r"artists", ArtistViewSet, basename="artists")
router.register(r"albums", AlbumViewSet, basename="albums")
router.register(r"audio", AudioViewSet, basename="audio")
router.register(r"artist_events", ArtistEventViewSet, basename="artist_events")
router.register(r"users", UserViewSet, basename="users")

urlpatterns = [
    url(r"^", include(router.urls)),
    url(r"^auth/", include("rest_framework.urls", namespace="rest_framework")),
    url(r"^token-auth/", obtain_auth_token),
    url(r"^register/", UserCreateView.as_view(), name='create-account'),
]
