from rest_framework import serializers
from django.contrib.auth.models import User
from marketplace.models import Programmer

class RegisterSerializer(serializers.Serializer):
    username = serializers.CharField()
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    user_type = serializers.CharField()

    category = serializers.CharField(required=False, allow_blank=True)
    description = serializers.CharField(required=False, allow_blank=True)
    skills = serializers.CharField(required=False, allow_blank=True)
    portfolio = serializers.CharField(required=False, allow_blank=True)
    imageUrl = serializers.CharField(required=False, allow_blank=True)

    def create(self, validated_data):
        user_type = validated_data.pop("user_type")
        username = validated_data.pop("username")
        email = validated_data.pop("email")
        password = validated_data.pop("password")

        # Create Django User
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
        )

        # Create freelancer profile
        if user_type == "freelancer":
            Programmer.objects.create(
                user=user,
                name=username,
                email=email,
                category=validated_data.get("category", ""),
                bio=validated_data.get("description", ""),
                skills=validated_data.get("skills", ""),
                portfolio=validated_data.get("portfolio", ""),
                image=validated_data.get("imageUrl", "")
            )

        return {
            "message": "Account created successfully",
            "username": username,
            "email": email,
            "user_type": user_type,
        }

# Serializer Password Change
class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)

    def validate_old_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError("Old password is incorrect.")
        return value