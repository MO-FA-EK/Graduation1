from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.core import exceptions as django_exceptions

from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class RegisterSerializer(serializers.ModelSerializer):
    """
    Serializer for user registration.
    """

    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ["id", "username", "email", "password"]

    def validate_email(self, value):
        if User.objects.filter(email__iexact=value).exists():
            raise serializers.ValidationError("A user with this email already exists.")
        return value

    def validate_password(self, value):
        """
        Run Django's password validators so weak passwords are rejected.
        """
        try:
            validate_password(value)
        except django_exceptions.ValidationError as e:
            raise serializers.ValidationError(e.messages)
        return value

    def create(self, validated_data):
        user = User(
            username=validated_data["username"],
            email=validated_data.get("email", ""),
        )
        user.set_password(validated_data["password"])
        user.save()
        return user


class UserTokenObtainPairSerializer(TokenObtainPairSerializer):
    """
    Custom login serializer:
    - Keeps SimpleJWT behaviour
    - Returns access, refresh, and a minimal 'user' object.
    """

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        # Optional: add extra info into the token payload if you want
        token["username"] = user.username
        return token

    def validate(self, attrs):
        # This will raise AuthenticationFailed if credentials are wrong.
        data = super().validate(attrs)

        user = self.user

        # Ensure response structure is exactly what we want:
        return {
            "access": data["access"],
            "refresh": data["refresh"],
            "user": {
                "id": user.id,
                "username": user.username,
                "email": user.email or "",
            },
        }
