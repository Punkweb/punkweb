from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework import serializers, viewsets, permissions, mixins, views
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken as OriginalObtain
from rest_framework.decorators import action
from rest_framework.response import Response
from easy_thumbnails.files import get_thumbnailer

from apps.music.models import (
    Artist,
    Album,
    Audio,
    ArtistEvent,
)

from punkweb.rest.permissions import IsTargetUser
from punkweb.rest import utils as rest_utils


class UserCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ('id', 'username', 'email', 'password')
        read_only_fields = ('id', )
        extra_kwargs = {
            'password': {'write_only': True},
        }

    def create(self, validated_data):
        user = get_user_model().objects.create_user(
            validated_data['username'],
            validated_data['email'],
            validated_data['password']
        )
        return user


class UserCreateView(views.APIView):
    def post(self, request):
        serializer = UserCreateSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            if user:
                return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


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

    @action(detail=False, methods=['get'])
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
    thumbnail = serializers.SerializerMethodField()

    class Meta:
        model = Artist
        fields = "__all__"
        lookup_field = 'slug'

    def get_thumbnail(self, obj):
        request = self.context.get('request')
        return request.build_absolute_uri(get_thumbnailer(obj.image)['avatar'].url)


class AlbumSerializer(serializers.ModelSerializer):
    artist_slug = serializers.SerializerMethodField()
    artist_name = serializers.SerializerMethodField()
    thumbnail = serializers.SerializerMethodField()

    class Meta:
        model = Album
        fields = "__all__"
        lookup_field = 'slug'

    def get_artist_slug(self, obj):
        return obj.artist.slug

    def get_artist_name(self, obj):
        return obj.artist.name

    def get_thumbnail(self, obj):
        request = self.context.get('request')
        return request.build_absolute_uri(get_thumbnailer(obj.cover_art)['avatar'].url)


class AudioSerializer(serializers.ModelSerializer):
    artist_name = serializers.SerializerMethodField()
    album_thumbnail = serializers.SerializerMethodField()

    class Meta:
        model = Audio
        fields = "__all__"

    def get_artist_name(self, obj):
        return obj.album.artist.name

    def get_thumbnail(self, obj):
        request = self.context.get('request')
        return request.build_absolute_uri(get_thumbnailer(obj.album.cover_art)['avatar'].url)


class ArtistEventSerializer(serializers.ModelSerializer):
    thumbnail = serializers.SerializerMethodField()

    class Meta:
        model = ArtistEvent
        fields = "__all__"

    def get_thumbnail(self, obj):
        request = self.context.get('request')
        return request.build_absolute_uri(get_thumbnailer(obj.event_image)['avatar'].url)


class ArtistViewSet(
    mixins.RetrieveModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet
):
    queryset = Artist.objects.none()
    serializer_class = ArtistSerializer
    lookup_field = 'slug'

    def get_queryset(self):
        qs = rest_utils.listed_artists(self.request)
        return qs.order_by("name")


class AlbumViewSet(
    mixins.RetrieveModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet
):
    queryset = Album.objects.none()
    serializer_class = AlbumSerializer
    lookup_field = 'slug'

    def get_serializer_context(self):
        context = super(AlbumViewSet, self).get_serializer_context()
        return context

    def get_queryset(self):
        qs = rest_utils.listed_albums(self.request)
        artist_id = self.request.query_params.get('artist_id')
        if artist_id:
            qs = qs.filter(artist__id=artist_id)
        return qs.order_by("artist", "title", "-release_date")

    @action(detail=False, methods=['get'])
    def latest_releases(self, request):
        qs = self.get_queryset().order_by("-release_date")[:5]
        serializer = self.get_serializer(qs.all(), many=True)
        return Response(serializer.data)


class AudioViewSet(
    mixins.RetrieveModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet
):
    queryset = Audio.objects.none()
    serializer_class = AudioSerializer

    def get_queryset(self):
        qs = rest_utils.listed_audio(self.request)
        artist_id = self.request.query_params.get('artist_id')
        if artist_id:
            qs = qs.filter(album__artist__id=artist_id)
        album_id = self.request.query_params.get('album_id')
        if album_id:
            qs = qs.filter(album__id=album_id)
        return qs.order_by(
            "disc_num",
            "track_num",
            "title",
        )


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
