from rest_framework import serializers
from .models import Programmer

class ProgrammerSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='name')  # send name as username
    imageUrl = serializers.CharField(source='image')  # match frontend
    totalRatings = serializers.IntegerField(source='review_count')

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
            'totalRatings'
        ]
