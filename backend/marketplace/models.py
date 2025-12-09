from django.db import models
from django.contrib.auth.models import User

class Programmer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    email = models.EmailField()
    category = models.CharField(max_length=255)
    bio = models.TextField(blank=True)
    skills = models.CharField(max_length=500)
    portfolio = models.CharField(max_length=500, blank=True)
    image = models.CharField(max_length=500, blank=True)
    rating = models.FloatField(default=0)
    review_count = models.IntegerField(default=0)
    profile_views = models.IntegerField(default=0)

    def __str__(self):
        return self.name
