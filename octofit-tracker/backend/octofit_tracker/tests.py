from django.test import TestCase
from django.utils import timezone
from datetime import date
from .models import User, Team, Activity, Leaderboard, Workout


class UserModelTest(TestCase):
    """Test cases for the User model"""
    
    def setUp(self):
        self.user = User.objects.create(
            email='test@example.com',
            name='Test User',
            team='Team Alpha',
            total_points=100
        )
    
    def test_user_creation(self):
        """Test that a user can be created successfully"""
        self.assertEqual(self.user.email, 'test@example.com')
        self.assertEqual(self.user.name, 'Test User')
        self.assertEqual(self.user.team, 'Team Alpha')
        self.assertEqual(self.user.total_points, 100)
        self.assertIsNotNone(self.user.created_at)
        self.assertIsNotNone(self.user.updated_at)
    
    def test_user_str(self):
        """Test the string representation of a user"""
        self.assertEqual(str(self.user), 'Test User')
    
    def test_user_email_unique(self):
        """Test that user email must be unique"""
        from django.db import IntegrityError
        with self.assertRaises(IntegrityError):
            User.objects.create(
                email='test@example.com',  # Duplicate email
                name='Another User'
            )


class TeamModelTest(TestCase):
    """Test cases for the Team model"""
    
    def setUp(self):
        self.team = Team.objects.create(
            name='Team Beta',
            description='A test team',
            total_points=500,
            member_count=5
        )
    
    def test_team_creation(self):
        """Test that a team can be created successfully"""
        self.assertEqual(self.team.name, 'Team Beta')
        self.assertEqual(self.team.description, 'A test team')
        self.assertEqual(self.team.total_points, 500)
        self.assertEqual(self.team.member_count, 5)
        self.assertIsNotNone(self.team.created_at)
        self.assertIsNotNone(self.team.updated_at)
    
    def test_team_str(self):
        """Test the string representation of a team"""
        self.assertEqual(str(self.team), 'Team Beta')
    
    def test_team_name_unique(self):
        """Test that team name must be unique"""
        from django.db import IntegrityError
        with self.assertRaises(IntegrityError):
            Team.objects.create(
                name='Team Beta',  # Duplicate name
                description='Another team'
            )


class ActivityModelTest(TestCase):
    """Test cases for the Activity model"""
    
    def setUp(self):
        self.activity = Activity.objects.create(
            user_email='user@example.com',
            user_name='Active User',
            team='Team Gamma',
            activity_type='Running',
            duration_minutes=30,
            points_earned=50,
            date=date.today(),
            notes='Morning run'
        )
    
    def test_activity_creation(self):
        """Test that an activity can be created successfully"""
        self.assertEqual(self.activity.user_email, 'user@example.com')
        self.assertEqual(self.activity.user_name, 'Active User')
        self.assertEqual(self.activity.team, 'Team Gamma')
        self.assertEqual(self.activity.activity_type, 'Running')
        self.assertEqual(self.activity.duration_minutes, 30)
        self.assertEqual(self.activity.points_earned, 50)
        self.assertEqual(self.activity.notes, 'Morning run')
        self.assertIsNotNone(self.activity.created_at)
    
    def test_activity_str(self):
        """Test the string representation of an activity"""
        expected = f"Active User - Running ({date.today()})"
        self.assertEqual(str(self.activity), expected)
    
    def test_activity_ordering(self):
        """Test that activities are ordered by date and created_at descending"""
        activity2 = Activity.objects.create(
            user_email='user@example.com',
            user_name='Active User',
            activity_type='Swimming',
            duration_minutes=45,
            points_earned=70,
            date=date.today()
        )
        activities = Activity.objects.all()
        # Most recent should be first
        self.assertEqual(activities[0].id, activity2.id)


class LeaderboardModelTest(TestCase):
    """Test cases for the Leaderboard model"""
    
    def setUp(self):
        self.leaderboard_entry = Leaderboard.objects.create(
            entity_type='user',
            entity_name='Top User',
            total_points=1000,
            rank=1,
            team='Team Delta'
        )
    
    def test_leaderboard_creation(self):
        """Test that a leaderboard entry can be created successfully"""
        self.assertEqual(self.leaderboard_entry.entity_type, 'user')
        self.assertEqual(self.leaderboard_entry.entity_name, 'Top User')
        self.assertEqual(self.leaderboard_entry.total_points, 1000)
        self.assertEqual(self.leaderboard_entry.rank, 1)
        self.assertEqual(self.leaderboard_entry.team, 'Team Delta')
        self.assertIsNotNone(self.leaderboard_entry.updated_at)
    
    def test_leaderboard_str(self):
        """Test the string representation of a leaderboard entry"""
        self.assertEqual(str(self.leaderboard_entry), 'Top User - Rank 1')
    
    def test_leaderboard_ordering(self):
        """Test that leaderboard entries are ordered by rank"""
        Leaderboard.objects.create(
            entity_type='user',
            entity_name='Second User',
            total_points=800,
            rank=2
        )
        Leaderboard.objects.create(
            entity_type='user',
            entity_name='Third User',
            total_points=600,
            rank=3
        )
        entries = Leaderboard.objects.all()
        self.assertEqual(entries[0].rank, 1)
        self.assertEqual(entries[1].rank, 2)
        self.assertEqual(entries[2].rank, 3)


class WorkoutModelTest(TestCase):
    """Test cases for the Workout model"""
    
    def setUp(self):
        self.workout = Workout.objects.create(
            name='Morning Cardio',
            description='High intensity cardio workout',
            difficulty_level='intermediate',
            estimated_duration_minutes=45,
            points_value=75,
            category='cardio',
            equipment_needed='Treadmill, Jump rope'
        )
    
    def test_workout_creation(self):
        """Test that a workout can be created successfully"""
        self.assertEqual(self.workout.name, 'Morning Cardio')
        self.assertEqual(self.workout.description, 'High intensity cardio workout')
        self.assertEqual(self.workout.difficulty_level, 'intermediate')
        self.assertEqual(self.workout.estimated_duration_minutes, 45)
        self.assertEqual(self.workout.points_value, 75)
        self.assertEqual(self.workout.category, 'cardio')
        self.assertEqual(self.workout.equipment_needed, 'Treadmill, Jump rope')
        self.assertIsNotNone(self.workout.created_at)
        self.assertIsNotNone(self.workout.updated_at)
    
    def test_workout_str(self):
        """Test the string representation of a workout"""
        self.assertEqual(str(self.workout), 'Morning Cardio')
    
    def test_workout_without_equipment(self):
        """Test creating a workout without equipment"""
        workout = Workout.objects.create(
            name='Bodyweight Training',
            description='No equipment needed',
            difficulty_level='beginner',
            estimated_duration_minutes=30,
            points_value=50,
            category='strength'
        )
        self.assertIsNone(workout.equipment_needed)
