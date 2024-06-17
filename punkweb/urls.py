"""
URL configuration for punkweb project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.contrib import admin
from django.contrib.staticfiles.urls import static
from django.urls import include, path
from rest_framework import routers

from apps.accounts.views import (
    LoginAPIView,
    LogoutAPIView,
    PasswordChangeAPIView,
    SessionAPIView,
    UserViewSet,
)
from apps.analytics.views import AnalyticsEventViewSet, ClientErrorViewSet
from apps.contact.views import ContactFormViewSet
from apps.music.views import (
    AlbumViewSet,
    ArtistEventViewSet,
    ArtistViewSet,
    AudioViewSet,
)

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
    path("admin/", admin.site.urls),
    path("api/", include(router.urls)),
    path("api/auth", include("rest_framework.urls")),
    path("api/login/", LoginAPIView.as_view(), name="login"),
    path("api/logout/", LogoutAPIView.as_view(), name="logout"),
    path(
        "api/password-change/", PasswordChangeAPIView.as_view(), name="password_change"
    ),
    path("api/session/", SessionAPIView.as_view(), name="session"),
    path("board/", include("punkweb_bb.urls")),
    path("insight/", include("punkweb_insight.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
