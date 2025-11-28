from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id',
            'name',
            'email',
            'skills',
            'image',
            'rating',
            'review_count',
            'category',
            'experience_level',
            'bio'
        ]
        read_only_fields = ["rating", "review_count"]

    # Name can’t be empty or too short
    def validate_name(self, value):
        value = value.strip()
        if len(value) < 2:
            raise serializers.ValidationError("Name must be at least 2 characters.")
        return value

    # Email must be valid + unique
    def validate_email(self, value):
        value = value.strip().lower()

        if not value:
            raise serializers.ValidationError("Email is required.")
        if "@" not in value:
            raise serializers.ValidationError("Enter a valid email address.")

        qs = User.objects.filter(email__iexact=value)

        # exclude yourself if updating profile
        if self.instance:
            qs = qs.exclude(id=self.instance.id)

        if qs.exists():
            raise serializers.ValidationError("Email already in use.")
        return value

    # Experience level must be controlled
    def validate_experience_level(self, value):
        allowed = ["Beginner", "Intermediate", "Advanced"]
        if value not in allowed:
            raise serializers.ValidationError(
                f"Experience level must be one of: {allowed}"
            )
        return value
