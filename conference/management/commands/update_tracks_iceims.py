from django.core.management.base import BaseCommand
from conference.models import ConferenceTrack

class Command(BaseCommand):
    help = 'Update conference tracks with ICEIMS 2026 data'

    def handle(self, *args, **kwargs):
        # Clear existing tracks
        ConferenceTrack.objects.all().delete()
        self.stdout.write('Cleared existing tracks')
        
        # Track 1 - Energy
        track1_topics = """Alternative fuels
Biogas and Biomass
Energy Storage Batteries and other Storage Devices
Fuel cell
Sustainable Hydrogen Technologies
Future Energy Technologies
Global warming & Green Energy Options
Health and Environment
Hybrid vehicles & Integration
Green Hydrogen
Energy Efficiency
Renewable Energy systems"""

        # Track 2 - Robotics
        track2_topics = """Industrial Robots and cobots
Drones and UAVs
Autonomous Wheeled mobile Robot
Agricultural robotics
Medical Robotics
Future Energy Technologies
Defense Robotics
Service Robotics"""

        # Track 3 - Manufacturing
        track3_topics = """CAD/CAM/CAE/CIM
Computational Mechanics & Techniques
Control and Automation
Flexible/ Lean Manufacturing
High-Speed/Precision Machining & Inspection
Measurement Control Technologies and Intelligent Systems
Mechatronics, MFMS and Nanotechnology
Metal Cutting and forming Processes
Modeling, Analysis & Simulation of Manufacturing Processes
Non-Conventional Machining Processes
Surface Engineering
Sustainable Manufacturing Technologies
Industrial Engineering & Management"""

        # Track 4 - Materials
        track4_topics = """Advanced High strength steels
New generation materials alloys
Biomaterials
Ceramic Materials
Characterization & Testing
Composite Materials
Dynamic Behavior of Materials and Structures
Functional Materials"""

        tracks_data = [
            {
                'track_number': 1,
                'title': 'Energy',
                'description': track1_topics,
                'track_type': 'regular',
            },
            {
                'track_number': 2,
                'title': 'Robotics',
                'description': track2_topics,
                'track_type': 'regular',
            },
            {
                'track_number': 3,
                'title': 'Manufacturing',
                'description': track3_topics,
                'track_type': 'regular',
            },
            {
                'track_number': 4,
                'title': 'Materials',
                'description': track4_topics,
                'track_type': 'regular',
            },
        ]
        
        created_count = 0
        for track_data in tracks_data:
            track = ConferenceTrack.objects.create(**track_data)
            self.stdout.write(self.style.SUCCESS(f'Created Track {track.track_number}: {track.title}'))
            created_count += 1
        
        self.stdout.write(self.style.SUCCESS(f'\nSuccessfully created {created_count} conference tracks!'))
