from rest_framework import serializers
from django.contrib.auth.models import User
from marketplace.models import Programmer
class UserSerializer(serializers.ModelSerializer):
    user_type = serializers.SerializerMethodField()
    
    def get_user_type(self, obj):
        if obj.is_superuser:
            return 'admin'
        

        try:
            if hasattr(obj, 'programmer') and obj.programmer:
                return 'freelancer'
        except Programmer.DoesNotExist:
            pass
        return 'client'
    
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'user_type', 'is_active', 'date_joined']
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

    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("A user with that username already exists.")
        return value

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("A user with that email already exists.")
        return value

    def create(self, validated_data):
        user_type = validated_data.pop("user_type")
        username = validated_data.pop("username")
        email = validated_data.pop("email")
        password = validated_data.pop("password")

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
        )

        if user_type == "freelancer":
            Programmer.objects.create(
                user=user,
                name=username,
                category=validated_data.get("category", ""),
                bio=validated_data.get("description", ""),
                skills=validated_data.get("skills", ""),
                experience_level="Junior", 
                hourly_rate=20.00, 
                portfolio_url=validated_data.get("portfolio", ""),
                image_url=validated_data.get("imageUrl", "")
            )

        return {
            "message": "Account created successfully",
            "username": username,
            "email": email,
            "user_type": user_type,
        }

class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)

    def validate_old_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError("Old password is incorrect.")
        return value