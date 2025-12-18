from rest_framework import serializers
from .models import Programmer, Project

class ProgrammerSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='name')
    imageUrl = serializers.CharField(source='image_url', required=False, allow_blank=True)
    portfolio = serializers.CharField(source='portfolio_url', required=False, allow_blank=True)
    totalRatings = serializers.IntegerField(source='review_count', read_only=True)
    profileViews = serializers.IntegerField(source='profile_views', read_only=True)
    
    email = serializers.EmailField(source='user.email', read_only=True)

    skills = serializers.SerializerMethodField()

    def get_skills(self, obj):
        if not obj.skills:
            return []

        return [s.strip() for s in obj.skills.split(",") if s.strip()]

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
            'hourly_rate',  
            'experience_level',
            'bank_name',
            'iban',
            'balance'
        ]

class ProjectSerializer(serializers.ModelSerializer):
    client_name = serializers.ReadOnlyField(source='client.username')
    freelancer_name = serializers.ReadOnlyField(source='freelancer.name')
    freelancer_id = serializers.ReadOnlyField(source='freelancer.id')

    class Meta:
        model = Project
        fields = [
            'id', 
            'client', 
            'client_name', 
            'freelancer', 
            'freelancer_name', 
            'freelancer_id', 
            'title', 
            'description', 
            'status', 
            'github_link', 
            'is_paid', 
            'amount', 
            'created_at'
        ]