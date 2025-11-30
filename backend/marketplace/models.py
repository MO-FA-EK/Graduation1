from django.db import models

class User(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    skills = models.TextField()  # will store comma-separated skills
    image = models.ImageField(upload_to="programmers/", blank=True, null=True)
    rating = models.FloatField(default=0.0)
    review_count = models.IntegerField(default=0)

    category = models.CharField(max_length=100, default="Web Developer")
    experience_level = models.CharField(max_length=20, default="Beginner")
    bio = models.TextField(blank=True, null=True)

    # NEW FIELDS to match frontend:
    portfolio = models.URLField(blank=True, null=True)
    profile_views = models.IntegerField(default=0)
    contact_clicks = models.IntegerField(default=0)

    def __str__(self):
        return self.name
