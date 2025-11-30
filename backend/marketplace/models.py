from django.db import models

# Create your models here.
class User(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    skills = models.TextField()   # simple for now, later could be ManyToMany
    image = models.ImageField(upload_to='profiles/', blank=True, null=True)
    rating = models.FloatField(default=0.0)
    review_count = models.IntegerField(default=0)

    # New fields
    category = models.CharField(max_length=100, default="General")  # e.g. Web Developer, Designer, Writer
    experience_level = models.CharField(max_length=50, default="Beginner")  # e.g. Beginner, Intermediate, Expert
    bio = models.TextField(blank=True, null=True)  # short description of the programmer

    def __str__(self):
        return self.name
