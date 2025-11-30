from rest_framework import serializers
from .models import User

class SkillsField(serializers.Field):
    """
    Custom field to store skills as a comma-separated string in the DB,
    but expose them as a list in the API.
    """

    def to_representation(self, value):
        # DB -> JSON
        if not value:
            return []
        return [s.strip() for s in str(value).split(",") if s.strip()]

    def to_internal_value(self, data):
        # JSON -> DB
        if isinstance(data, list):
            # convert ["A", "B"] -> "A, B"
            return ", ".join(str(s).strip() for s in data if str(s).strip())
        if isinstance(data, str):
            # already a string
            return data.strip()
        raise serializers.ValidationError("Skills must be a list or a string.")


class UserSerializer(serializers.ModelSerializer):
    # Map backend field names to what frontend expects
    username = serializers.CharField(source="name")
    description = serializers.CharField(
        source="bio", allow_blank=True, allow_null=True
    )
    imageUrl = serializers.ImageField(
        source="image", allow_null=True, required=False
    )
    totalRatings = serializers.IntegerField(
        source="review_count", read_only=True
    )
    profileViews = serializers.IntegerField(
        source="profile_views", read_only=True
    )
    contactClicks = serializers.IntegerField(
        source="contact_clicks", read_only=True
    )

    # NEW: use our custom field here
    skills = SkillsField()

    class Meta:
        model = User
        fields = [
            "id",
            "username",        # from name
            "email",
            "category",
            "description",     # from bio
            "skills",          # custom field
            "portfolio",
            "imageUrl",        # from image
            "rating",
            "totalRatings",    # from review_count
            "profileViews",    # from profile_views
            "contactClicks",   # from contact_clicks
            "experience_level",
        ]

    def validate_email(self, value):
        """
        Make sure email is unique (except for current instance on update).
        """
        qs = User.objects.filter(email__iexact=value)
        if self.instance:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise serializers.ValidationError("A user with this email already exists.")
        return value

    def validate_experience_level(self, value):
        allowed = ["Beginner", "Intermediate", "Advanced"]
        if value not in allowed:
            raise serializers.ValidationError(
                f"experience_level must be one of: {', '.join(allowed)}"
            )
        return value
