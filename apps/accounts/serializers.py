from django.contrib.auth import authenticate, get_user_model, update_session_auth_hash
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers


User = get_user_model()


def validate_passwords_match(password1, password2):
    if password1 != password2:
        raise serializers.ValidationError("Passwords do not match.")


class PasswordField(serializers.CharField):
    def __init__(self, **kwargs):
        kwargs.setdefault("style", {})
        kwargs["style"] = {"input_type": "password"}
        kwargs["trim_whitespace"] = False
        kwargs["write_only"] = True
        super().__init__(**kwargs)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ("password",)
        read_only_fields = (
            "last_login",
            "is_superuser",
            "username",
            "email",
            "is_staff",
            "is_active",
            "date_joined",
            "groups",
            "user_permissions",
        )


class UserCreateSerializer(serializers.Serializer):
    username = serializers.CharField(label="Username", max_length=150)
    password1 = PasswordField(label="Password")
    password2 = PasswordField(label="Password (again)")

    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError(
                "A user with that username already exists."
            )
        return value

    def validate(self, data):
        validate_passwords_match(data["password1"], data["password2"])
        validate_password(data["password1"])
        return data

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data["username"],
            password=validated_data["password1"],
        )
        return user


class AuthenticationSerializer(serializers.Serializer):
    username = serializers.CharField(label="Username", max_length=150)
    password = PasswordField(label="Password")

    def validate(self, data):
        username = data.get("username")
        password = data.get("password")
        request = self.context.get("request")

        user = authenticate(request=request, username=username, password=password)

        if not user:
            raise serializers.ValidationError(
                "Unable to log in with provided credentials."
            )

        data["user"] = user
        return data


class PasswordChangeSerializer(serializers.Serializer):
    current_password = PasswordField(label="Current password")
    new_password1 = PasswordField(label="New password")
    new_password2 = PasswordField(label="New password (again)")

    def validate_current_password(self, value):
        request = self.context.get("request")
        user = request.user
        if not user.check_password(value):
            raise serializers.ValidationError("The current password was incorrect.")

    def validate(self, data):
        validate_passwords_match(data["new_password1"], data["new_password2"])
        validate_password(data["new_password1"])
        return data

    def save(self):
        request = self.context.get("request")

        user = request.user
        user.set_password(self.validated_data["new_password1"])
        user.save()

        update_session_auth_hash(request, user)

        return user
