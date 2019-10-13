from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework import serializers, viewsets, permissions, mixins, views
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken as OriginalObtain
from rest_framework.decorators import action, list_route
from rest_framework.response import Response

from apps.music.models import (
    Artist,
    Album,
    Audio,
    ArtistEvent,
)

from apps.rest.permissions import IsTargetUser


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        exclude = ("password", "groups", "user_permissions")
        read_only_fields = (
            "last_login",
            "date_joined",
            "is_staff",
            "is_superuser",
            "email",
            "username",
        )


class UserViewSet(
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet,
):
    queryset = get_user_model().objects.order_by("username")
    serializer_class = UserSerializer
    permission_classes = (permissions.IsAuthenticated, IsTargetUser)

    @list_route()
    def from_token(self, request, *args, **kwargs):
        token_string = request.query_params.get("token")
        if not token_string:
            return Response("Token query param required", status=400)

        token = get_object_or_404(Token, key=token_string)
        self.kwargs["pk"] = token.user_id
        user = self.get_object()
        return Response(self.get_serializer(user).data)


class ObtainAuthToken(OriginalObtain):
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        token, created = Token.objects.get_or_create(user=user)
        return Response({"token": token.key, "id": user.id})


obtain_auth_token = ObtainAuthToken.as_view()


class ArtistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Artist
        fields = "__all__"
        lookup_field = 'slug'


class AlbumSerializer(serializers.ModelSerializer):
    artist_slug = serializers.SerializerMethodField()

    class Meta:
        model = Album
        fields = "__all__"
        lookup_field = 'slug'

    def get_artist_slug(self, obj):
        return obj.artist.slug


class AudioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Audio
        fields = "__all__"


class ArtistEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = ArtistEvent
        fields = "__all__"


class ArtistViewSet(
    mixins.RetrieveModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet
):
    queryset = Artist.objects.order_by("name")
    serializer_class = ArtistSerializer
    lookup_field = 'slug'

    def get_queryset(self):
        qs = self.queryset
        return qs.all()


class AlbumViewSet(
    mixins.RetrieveModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet
):
    queryset = Album.objects.order_by("artist", "title", "-release_date")
    serializer_class = AlbumSerializer
    lookup_field = 'slug'

    def get_queryset(self):
        qs = self.queryset
        artist_id = self.request.query_params.get('artist_id')
        if artist_id:
            qs = qs.filter(artist__id=artist_id)
        return qs.all()

    @action(detail=False, methods=['get'])
    def latest_releases(self, request):
        qs = self.get_queryset()
        return Response(qs.order_by("-release_date")[:5])


class AudioViewSet(
    mixins.RetrieveModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet
):
    queryset = Audio.objects.order_by(
        "disc_num",
        "track_num",
        "title",
    )
    serializer_class = AudioSerializer

    def get_queryset(self):
        qs = self.queryset
        artist_id = self.request.query_params.get('artist_id')
        if artist_id:
            qs = qs.filter(album__artist__id=artist_id)
        return qs.all()


class ArtistEventViewSet(
    mixins.RetrieveModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet
):
    queryset = ArtistEvent.objects.order_by("-event_date")
    serializer_class = ArtistEventSerializer

    def get_queryset(self):
        qs = self.queryset
        artist_id = self.request.query_params.get('artist_id')
        if artist_id:
            qs = qs.filter(artist__id=artist_id)
        return qs.all()
