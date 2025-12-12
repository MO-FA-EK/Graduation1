from rest_framework import serializers
from .models import Programmer

class ProgrammerSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='name')
    imageUrl = serializers.CharField(source='image')
    totalRatings = serializers.IntegerField(source='review_count', read_only=True)

    profileViews = serializers.IntegerField(source='profile_views', read_only=True)
    contactClicks = serializers.IntegerField(source='contact_clicks', read_only=True)

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
            'bio',
            'skills',
            'portfolio',
            'imageUrl',
            'rating',
            'totalRatings',
            'profileViews',
            'contactClicks',
        ]
