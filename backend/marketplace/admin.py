from django.contrib import admin
from .models import Programmer, Project


@admin.register(Programmer)
class ProgrammerAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'category', 'experience_level', 'hourly_rate', 'rating', 'profile_views')
    list_filter = ('category', 'experience_level')
    search_fields = ('name', 'category', 'skills')
    ordering = ('-profile_views', '-rating')
    readonly_fields = ('profile_views', 'rating', 'review_count')

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'client', 'freelancer', 'status', 'is_paid', 'amount', 'created_at')
    list_filter = ('status', 'is_paid', 'created_at')
    search_fields = ('title', 'description', 'client__username', 'freelancer__name')
    ordering = ('-created_at',)
