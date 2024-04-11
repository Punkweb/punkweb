from django.contrib.auth import get_user_model, login, logout
from rest_framework import permissions, status, views, viewsets
from rest_framework.response import Response

from apps.accounts.permissions import UserPermission
from apps.accounts.serializers import (
    AuthenticationSerializer,
    PasswordChangeSerializer,
    UserCreateSerializer,
    UserSerializer,
)

User = get_user_model()


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (UserPermission,)

    def get_serializer_class(self):
        if self.action == "create":
            return UserCreateSerializer
        return self.serializer_class

    def get_queryset(self):
        qs = self.queryset
        qs = qs.filter(id=self.request.user.id)
        return qs

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response(UserSerializer(user).data, status=status.HTTP_201_CREATED)


class LoginAPIView(views.APIView):
    serializer_class = AuthenticationSerializer
    permission_classes = (permissions.AllowAny,)

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(
            data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        login(request, user)
        data = UserSerializer(user).data
        return Response(data)


class LogoutAPIView(views.APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        logout(request)
        return Response(status=status.HTTP_204_NO_CONTENT)


class SessionAPIView(views.APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        user = UserSerializer(request.user, context={"request": request}).data
        return Response(user)


class PasswordChangeAPIView(views.APIView):
    serializer_class = PasswordChangeSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(
            data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=status.HTTP_204_NO_CONTENT)
