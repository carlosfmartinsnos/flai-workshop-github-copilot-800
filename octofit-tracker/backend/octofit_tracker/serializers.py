from rest_framework import serializers
from .models import User, Team, Activity, Leaderboard, Workout


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'name', 'team', 'total_points', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']


class TeamSerializer(serializers.ModelSerializer):
    member_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Team
        fields = ['id', 'name', 'description', 'total_points', 'member_count', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def get_member_count(self, obj):
        """Dynamically calculate member count from User model"""
        return User.objects.filter(team=obj.name).count()


class ActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Activity
        fields = ['id', 'user_email', 'user_name', 'team', 'activity_type', 'duration_minutes', 
                  'points_earned', 'date', 'notes', 'created_at']
        read_only_fields = ['id', 'created_at']


class LeaderboardSerializer(serializers.ModelSerializer):
    activities_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Leaderboard
        fields = ['id', 'entity_type', 'entity_name', 'total_points', 'rank', 'team', 'activities_count', 'updated_at']
        read_only_fields = ['id', 'updated_at']
    
    def get_activities_count(self, obj):
        """Get the count of activities for this user"""
        if obj.entity_type == 'user':
            # Find user by name and get their activity count
            user = User.objects.filter(name=obj.entity_name).first()
            if user:
                return Activity.objects.filter(user_email=user.email).count()
        return 0


class WorkoutSerializer(serializers.ModelSerializer):
    class Meta:
        model = Workout
        fields = ['id', 'name', 'description', 'difficulty_level', 'estimated_duration_minutes', 
                  'points_value', 'category', 'equipment_needed', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']
