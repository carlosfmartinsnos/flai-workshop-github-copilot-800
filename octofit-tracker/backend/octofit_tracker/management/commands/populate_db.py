from django.core.management.base import BaseCommand
from octofit_tracker.models import User, Team, Activity, Leaderboard, Workout
from datetime import date, timedelta


class Command(BaseCommand):
    help = 'Populate the octofit_db database with test data'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.SUCCESS('Starting database population...'))

        # Clear existing data
        self.stdout.write('Clearing existing data...')
        User.objects.all().delete()
        Team.objects.all().delete()
        Activity.objects.all().delete()
        Leaderboard.objects.all().delete()
        Workout.objects.all().delete()

        # Create Teams
        self.stdout.write('Creating teams...')
        team_marvel = Team.objects.create(
            name='Team Marvel',
            description='Earth\'s Mightiest Heroes',
            total_points=0,
            member_count=0
        )
        team_dc = Team.objects.create(
            name='Team DC',
            description='Justice League Members',
            total_points=0,
            member_count=0
        )

        # Create Marvel Users
        self.stdout.write('Creating Marvel superheroes...')
        marvel_users = [
            User.objects.create(
                email='ironman@marvel.com',
                name='Iron Man (Tony Stark)',
                team='Team Marvel',
                total_points=350
            ),
            User.objects.create(
                email='captain.america@marvel.com',
                name='Captain America (Steve Rogers)',
                team='Team Marvel',
                total_points=420
            ),
            User.objects.create(
                email='thor@marvel.com',
                name='Thor Odinson',
                team='Team Marvel',
                total_points=380
            ),
            User.objects.create(
                email='hulk@marvel.com',
                name='Hulk (Bruce Banner)',
                team='Team Marvel',
                total_points=290
            ),
            User.objects.create(
                email='black.widow@marvel.com',
                name='Black Widow (Natasha Romanoff)',
                team='Team Marvel',
                total_points=310
            ),
        ]

        # Create DC Users
        self.stdout.write('Creating DC superheroes...')
        dc_users = [
            User.objects.create(
                email='superman@dc.com',
                name='Superman (Clark Kent)',
                team='Team DC',
                total_points=450
            ),
            User.objects.create(
                email='batman@dc.com',
                name='Batman (Bruce Wayne)',
                team='Team DC',
                total_points=410
            ),
            User.objects.create(
                email='wonder.woman@dc.com',
                name='Wonder Woman (Diana Prince)',
                team='Team DC',
                total_points=390
            ),
            User.objects.create(
                email='flash@dc.com',
                name='The Flash (Barry Allen)',
                team='Team DC',
                total_points=360
            ),
            User.objects.create(
                email='aquaman@dc.com',
                name='Aquaman (Arthur Curry)',
                team='Team DC',
                total_points=280
            ),
        ]

        all_users = marvel_users + dc_users

        # Update team totals
        team_marvel.member_count = len(marvel_users)
        team_marvel.total_points = sum(u.total_points for u in marvel_users)
        team_marvel.save()

        team_dc.member_count = len(dc_users)
        team_dc.total_points = sum(u.total_points for u in dc_users)
        team_dc.save()

        # Create Activities
        self.stdout.write('Creating activities...')
        today = date.today()
        
        activities_data = [
            # Marvel activities
            ('ironman@marvel.com', 'Iron Man (Tony Stark)', 'Team Marvel', 'Tech Training', 60, 50),
            ('ironman@marvel.com', 'Iron Man (Tony Stark)', 'Team Marvel', 'Flight Simulation', 90, 70),
            ('captain.america@marvel.com', 'Captain America (Steve Rogers)', 'Team Marvel', 'Combat Training', 120, 100),
            ('captain.america@marvel.com', 'Captain America (Steve Rogers)', 'Team Marvel', 'Shield Practice', 75, 60),
            ('thor@marvel.com', 'Thor Odinson', 'Team Marvel', 'Hammer Training', 90, 80),
            ('thor@marvel.com', 'Thor Odinson', 'Team Marvel', 'Lightning Control', 60, 50),
            ('hulk@marvel.com', 'Hulk (Bruce Banner)', 'Team Marvel', 'Strength Training', 45, 40),
            ('hulk@marvel.com', 'Hulk (Bruce Banner)', 'Team Marvel', 'Meditation', 30, 20),
            ('black.widow@marvel.com', 'Black Widow (Natasha Romanoff)', 'Team Marvel', 'Espionage Training', 120, 100),
            ('black.widow@marvel.com', 'Black Widow (Natasha Romanoff)', 'Team Marvel', 'Martial Arts', 90, 70),
            # DC activities
            ('superman@dc.com', 'Superman (Clark Kent)', 'Team DC', 'Flight Training', 120, 100),
            ('superman@dc.com', 'Superman (Clark Kent)', 'Team DC', 'Super Strength', 90, 80),
            ('batman@dc.com', 'Batman (Bruce Wayne)', 'Team DC', 'Detective Work', 150, 120),
            ('batman@dc.com', 'Batman (Bruce Wayne)', 'Team DC', 'Combat Training', 100, 80),
            ('wonder.woman@dc.com', 'Wonder Woman (Diana Prince)', 'Team DC', 'Lasso Training', 75, 60),
            ('wonder.woman@dc.com', 'Wonder Woman (Diana Prince)', 'Team DC', 'Amazon Combat', 105, 90),
            ('flash@dc.com', 'The Flash (Barry Allen)', 'Team DC', 'Speed Training', 120, 100),
            ('flash@dc.com', 'The Flash (Barry Allen)', 'Team DC', 'Cardio Sprint', 90, 70),
            ('aquaman@dc.com', 'Aquaman (Arthur Curry)', 'Team DC', 'Swimming', 90, 70),
            ('aquaman@dc.com', 'Aquaman (Arthur Curry)', 'Team DC', 'Trident Training', 60, 50),
        ]

        for i, (email, name, team, activity_type, duration, points) in enumerate(activities_data):
            Activity.objects.create(
                user_email=email,
                user_name=name,
                team=team,
                activity_type=activity_type,
                duration_minutes=duration,
                points_earned=points,
                date=today - timedelta(days=i % 7),
                notes=f'Training session for {activity_type.lower()}'
            )

        # Create Leaderboard entries
        self.stdout.write('Creating leaderboard entries...')
        
        # Sort users by points
        sorted_users = sorted(all_users, key=lambda u: u.total_points, reverse=True)
        for rank, user in enumerate(sorted_users, start=1):
            Leaderboard.objects.create(
                entity_type='user',
                entity_name=user.name,
                total_points=user.total_points,
                rank=rank,
                team=user.team
            )

        # Team leaderboard
        teams = [team_dc, team_marvel]
        sorted_teams = sorted(teams, key=lambda t: t.total_points, reverse=True)
        for rank, team in enumerate(sorted_teams, start=1):
            Leaderboard.objects.create(
                entity_type='team',
                entity_name=team.name,
                total_points=team.total_points,
                rank=rank
            )

        # Create Workouts
        self.stdout.write('Creating workout suggestions...')
        workouts_data = [
            {
                'name': 'Super Soldier Serum Training',
                'description': 'High-intensity training based on Captain America\'s regimen',
                'difficulty_level': 'advanced',
                'estimated_duration_minutes': 90,
                'points_value': 100,
                'category': 'strength',
                'equipment_needed': 'Weights, resistance bands, pull-up bar'
            },
            {
                'name': 'Speedster Sprint Challenge',
                'description': 'Quick cardio bursts inspired by The Flash',
                'difficulty_level': 'intermediate',
                'estimated_duration_minutes': 45,
                'points_value': 60,
                'category': 'cardio',
                'equipment_needed': 'Running track or treadmill'
            },
            {
                'name': 'Amazonian Warrior Workout',
                'description': 'Combat-ready strength and flexibility training like Wonder Woman',
                'difficulty_level': 'advanced',
                'estimated_duration_minutes': 75,
                'points_value': 85,
                'category': 'strength',
                'equipment_needed': 'Dumbbells, yoga mat'
            },
            {
                'name': 'Web-Slinger Flexibility',
                'description': 'Spider-Man inspired flexibility and agility routine',
                'difficulty_level': 'beginner',
                'estimated_duration_minutes': 30,
                'points_value': 40,
                'category': 'flexibility',
                'equipment_needed': 'Yoga mat'
            },
            {
                'name': 'Dark Knight Detective Training',
                'description': 'Batman\'s full-body conditioning program',
                'difficulty_level': 'advanced',
                'estimated_duration_minutes': 120,
                'points_value': 130,
                'category': 'strength',
                'equipment_needed': 'Complete gym setup'
            },
            {
                'name': 'Asgardian Power Lift',
                'description': 'Thor-inspired heavy lifting routine',
                'difficulty_level': 'advanced',
                'estimated_duration_minutes': 60,
                'points_value': 80,
                'category': 'strength',
                'equipment_needed': 'Barbells, weight plates'
            },
            {
                'name': 'Aquatic Endurance',
                'description': 'Swimming workout inspired by Aquaman',
                'difficulty_level': 'intermediate',
                'estimated_duration_minutes': 60,
                'points_value': 70,
                'category': 'cardio',
                'equipment_needed': 'Swimming pool'
            },
            {
                'name': 'Spy Agility Training',
                'description': 'Black Widow\'s stealth and agility workout',
                'difficulty_level': 'intermediate',
                'estimated_duration_minutes': 50,
                'points_value': 65,
                'category': 'flexibility',
                'equipment_needed': 'Minimal equipment, bodyweight focus'
            },
        ]

        for workout_data in workouts_data:
            Workout.objects.create(**workout_data)

        self.stdout.write(self.style.SUCCESS(
            f'\nDatabase populated successfully!\n'
            f'Users: {User.objects.count()}\n'
            f'Teams: {Team.objects.count()}\n'
            f'Activities: {Activity.objects.count()}\n'
            f'Leaderboard entries: {Leaderboard.objects.count()}\n'
            f'Workouts: {Workout.objects.count()}'
        ))
