from rest_framework import serializers
from .models import Programmer, Rating


class ProgrammerSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='name')
    imageUrl = serializers.CharField(source='image')

    # Computed fields
    rating = serializers.FloatField(source='average_rating', read_only=True)
    totalRatings = serializers.IntegerField(source='total_ratings', read_only=True)

    profileViews = serializers.IntegerField(source='profile_views', read_only=True)
    contactClicks = serializers.IntegerField(source='contact_clicks', read_only=True)

    # FRONTEND EXPECTS description → map to backend bio
    description = serializers.CharField(source='bio', allow_blank=True)

    # Convert comma-separated → list
    skills = serializers.SerializerMethodField()

    def get_skills(self, obj):
        if not obj.skills:
            return []
        return [s.strip() for s in obj.skills.split(",")]

    class Meta:
        model = Programmer
        fields = [
            'id',
            'username',
            'email',
            'category',
            'description',   # <-- ADDED (alias to bio)
            'skills',
            'portfolio',
            'imageUrl',
            'rating',
            'totalRatings',
            'profileViews',
            'contactClicks',
        ]
