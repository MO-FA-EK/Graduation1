from rest_framework import serializers
from .models import User


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

    class Meta:
        model = User
        fields = [
            "id",
            "username",       # from name
            "email",
            "category",
            "description",    # from bio
            "skills",         # handled specially below
            "portfolio",
            "imageUrl",       # from image
            "rating",
            "totalRatings",   # from review_count
            "profileViews",   # from profile_views
            "contactClicks",  # from contact_clicks
            "experience_level",  # extra field, frontend can ignore for now
        ]

    # --- VALIDATIONS YOU ALREADY HAD, ADAPTED ---

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

    # --- SKILLS: store as text in DB, send as list[] to frontend ---

    def to_representation(self, instance):
        """
        Convert DB -> JSON.
        skills: "A, B, C" -> ["A", "B", "C"]
        """
        data = super().to_representation(instance)
        skills_text = instance.skills or ""
        if skills_text.strip():
            data["skills"] = [
                s.strip() for s in skills_text.split(",") if s.strip()
            ]
        else:
            data["skills"] = []
        return data

    def _normalize_skills(self, skills):
        """
        Convert incoming JSON value for skills -> text for DB.
        Accepts list or string.
        """
        if isinstance(skills, list):
            return ", ".join(str(s).strip() for s in skills if str(s).strip())
        # string or anything else
        return str(skills).strip()

    def create(self, validated_data):
        # validated_data['skills'] might be list or string
        skills = validated_data.get("skills")
        if skills is not None:
            validated_data["skills"] = self._normalize_skills(skills)
        return super().create(validated_data)

    def update(self, instance, validated_data):
        skills = validated_data.get("skills", None)
        if skills is not None:
            validated_data["skills"] = self._normalize_skills(skills)
        return super().update(instance, validated_data)
