from django.db import models
from django.contrib.auth.models import User


class Programmer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    # Basic profile fields
    name = models.CharField(max_length=255)
    email = models.EmailField()
    category = models.CharField(max_length=255)
    bio = models.TextField(blank=True)

    # Comma-separated string → frontend converts to list
    skills = models.CharField(max_length=500)

    portfolio = models.CharField(max_length=500, blank=True)
    image = models.CharField(max_length=500, blank=True)

    # Tracking fields
    profile_views = models.PositiveIntegerField(default=0)
    contact_clicks = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.name

    # ------- Rating Computations -------
    @property
    def average_rating(self):
        """Return computed average rating as float, rounded to 1 decimal."""
        qs = self.ratings.all()
        if not qs.exists():
            return 0
        return round(sum(r.stars for r in qs) / qs.count(), 1)

    @property
    def total_ratings(self):
        """Return count of unique user ratings."""
        return self.ratings.count()


class Rating(models.Model):
    programmer = models.ForeignKey(
        Programmer,
        on_delete=models.CASCADE,
        related_name="ratings"
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    # Store rating 1–5
    stars = models.PositiveIntegerField()

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        # Ensure one rating per user per programmer
        unique_together = ('programmer', 'user')

    def __str__(self):
        return f"{self.user.username} → {self.programmer.name}: {self.stars}⭐"
