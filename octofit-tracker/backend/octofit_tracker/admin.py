from django.contrib import admin
from .models import User, Team, Activity, Leaderboard, Workout


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    """Admin interface for User model"""
    list_display = ('id', 'name', 'email', 'team', 'total_points', 'created_at')
    list_filter = ('team', 'created_at')
    search_fields = ('name', 'email', 'team')
    ordering = ('-total_points', 'name')
    readonly_fields = ('created_at', 'updated_at')
    
    fieldsets = (
        ('User Information', {
            'fields': ('email', 'name', 'team')
        }),
        ('Statistics', {
            'fields': ('total_points',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    """Admin interface for Team model"""
    list_display = ('id', 'name', 'member_count', 'total_points', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('name', 'description')
    ordering = ('-total_points', 'name')
    readonly_fields = ('created_at', 'updated_at')
    
    fieldsets = (
        ('Team Information', {
            'fields': ('name', 'description')
        }),
        ('Statistics', {
            'fields': ('member_count', 'total_points')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(Activity)
class ActivityAdmin(admin.ModelAdmin):
    """Admin interface for Activity model"""
    list_display = ('id', 'user_name', 'activity_type', 'duration_minutes', 
                    'points_earned', 'date', 'team', 'created_at')
    list_filter = ('activity_type', 'team', 'date', 'created_at')
    search_fields = ('user_name', 'user_email', 'activity_type', 'team', 'notes')
    ordering = ('-date', '-created_at')
    readonly_fields = ('created_at',)
    date_hierarchy = 'date'
    
    fieldsets = (
        ('User Information', {
            'fields': ('user_email', 'user_name', 'team')
        }),
        ('Activity Details', {
            'fields': ('activity_type', 'duration_minutes', 'points_earned', 'date', 'notes')
        }),
        ('Timestamp', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )


@admin.register(Leaderboard)
class LeaderboardAdmin(admin.ModelAdmin):
    """Admin interface for Leaderboard model"""
    list_display = ('id', 'entity_name', 'entity_type', 'rank', 'total_points', 'team', 'updated_at')
    list_filter = ('entity_type', 'team', 'updated_at')
    search_fields = ('entity_name', 'team')
    ordering = ('rank',)
    readonly_fields = ('updated_at',)
    
    fieldsets = (
        ('Leaderboard Entry', {
            'fields': ('entity_type', 'entity_name', 'rank', 'team')
        }),
        ('Statistics', {
            'fields': ('total_points',)
        }),
        ('Timestamp', {
            'fields': ('updated_at',),
            'classes': ('collapse',)
        }),
    )


@admin.register(Workout)
class WorkoutAdmin(admin.ModelAdmin):
    """Admin interface for Workout model"""
    list_display = ('id', 'name', 'category', 'difficulty_level', 
                    'estimated_duration_minutes', 'points_value', 'created_at')
    list_filter = ('difficulty_level', 'category', 'created_at')
    search_fields = ('name', 'description', 'category', 'equipment_needed')
    ordering = ('difficulty_level', 'category', 'name')
    readonly_fields = ('created_at', 'updated_at')
    
    fieldsets = (
        ('Workout Information', {
            'fields': ('name', 'description', 'category')
        }),
        ('Workout Details', {
            'fields': ('difficulty_level', 'estimated_duration_minutes', 
                      'points_value', 'equipment_needed')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
