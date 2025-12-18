from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Programmer(models.Model):
    EXPERIENCE_CHOICES = [
        ('Junior', 'Junior'),
        ('Mid-Level', 'Mid-Level'),
        ('Senior', 'Senior'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='programmer', null=True, blank=True)
    name = models.CharField(max_length=100)
    category = models.CharField(max_length=100)  
    skills = models.TextField()  
    experience_level = models.CharField(max_length=20, choices=EXPERIENCE_CHOICES, default='Junior')
    bio = models.TextField(blank=True)
    hourly_rate = models.DecimalField(max_digits=6, decimal_places=2)
    image_url = models.URLField(max_length=500, blank=True)
    portfolio_url = models.URLField(max_length=500, blank=True)

    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    
    bank_name = models.CharField(max_length=100, blank=True, default='')
    iban = models.CharField(max_length=50, blank=True, default='')
    
    rating = models.FloatField(default=0.0)
    review_count = models.IntegerField(default=0)
    profile_views = models.IntegerField(default=0)
    
    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return f"/freelancer/{self.id}"


class Project(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('active', 'Active'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    )

    client = models.ForeignKey(User, related_name='hired_projects', on_delete=models.CASCADE)
    freelancer = models.ForeignKey(Programmer, related_name='work_projects', on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    github_link = models.URLField(blank=True, null=True)
    
    is_paid = models.BooleanField(default=False)
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=50.00)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} ({self.status})"
        
    def get_absolute_url(self):
        return f"/admin/marketplace/project/{self.id}/change/"