from django.db import models

class User(models.Model):
    email = models.EmailField(unique=True, max_length=255)
    name = models.CharField(max_length=255)
    team = models.CharField(max_length=255, blank=True, null=True)
    total_points = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'users'

    def __str__(self):
        return self.name


class Team(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True, null=True)
    total_points = models.IntegerField(default=0)
    member_count = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'teams'

    def __str__(self):
        return self.name


class Activity(models.Model):
    user_email = models.EmailField(max_length=255)
    user_name = models.CharField(max_length=255)
    team = models.CharField(max_length=255, blank=True, null=True)
    activity_type = models.CharField(max_length=100)
    duration_minutes = models.IntegerField()
    points_earned = models.IntegerField()
    date = models.DateField()
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'activities'
        ordering = ['-date', '-created_at']

    def __str__(self):
        return f"{self.user_name} - {self.activity_type} ({self.date})"


class Leaderboard(models.Model):
    entity_type = models.CharField(max_length=50)  # 'user' or 'team'
    entity_name = models.CharField(max_length=255)
    total_points = models.IntegerField()
    rank = models.IntegerField()
    team = models.CharField(max_length=255, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'leaderboard'
        ordering = ['rank']

    def __str__(self):
        return f"{self.entity_name} - Rank {self.rank}"


class Workout(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    difficulty_level = models.CharField(max_length=50)  # 'beginner', 'intermediate', 'advanced'
    estimated_duration_minutes = models.IntegerField()
    points_value = models.IntegerField()
    category = models.CharField(max_length=100)  # 'strength', 'cardio', 'flexibility', etc.
    equipment_needed = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'workouts'

    def __str__(self):
        return self.name
