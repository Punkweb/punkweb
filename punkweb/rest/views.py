import time

from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework import mixins, permissions, views, viewsets
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken as OriginalObtain
from rest_framework.decorators import action
from rest_framework.response import Response

from punkweb.rest.permissions import IsTargetUser
from punkweb.rest.serializers import UserCreateSerializer, UserSerializer

reg_fingerprints = []


class UserCreateView(views.APIView):
    def post(self, request):
        serializer = UserCreateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=409)

        # ----------------------------------
        # If the same ip has reg'd an account in the past two minutes,
        # return 401. Their ip is removed from the list when another
        # request has been made and more than two minutes has passed.
        forwarded = request.META.get("HTTP_X_FORWARDED_FOR")
        if forwarded:
            ip = forwarded.split(",")[-1].strip()
        else:
            ip = request.META.get("REMOTE_ADDR")

        for fp in reg_fingerprints:
            if fp.get("ip") == ip:
                if time.time() - fp.get("timestamp") > 120:
                    reg_fingerprints.remove(fp)
                else:
                    return Response("Spam detected", status=401)

        reg_fingerprints.append({"ip": ip, "timestamp": time.time()})
        # ----------------------------------

        user = serializer.save()
        if user:
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


class UserViewSet(
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet,
):
    queryset = get_user_model().objects.order_by("username")
    serializer_class = UserSerializer
    permission_classes = (permissions.IsAuthenticated, IsTargetUser)

    @action(detail=False, methods=["get"])
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
        token, _ = Token.objects.get_or_create(user=user)
        return Response({"token": token.key, "id": user.id})


obtain_auth_token = ObtainAuthToken.as_view()
