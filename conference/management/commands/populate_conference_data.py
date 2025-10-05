"""
Management command to populate conference data
Run with: python manage.py populate_conference_data
"""
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from conference.models import (
    Speaker, CommitteeMember, Schedule, ImportantDate, 
    ConferenceTrack, ConferenceSettings
)
from datetime import datetime, time, date


class Command(BaseCommand):
    help = 'Populates the database with conference data'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.SUCCESS('Starting data population...'))
        
        # Clear existing data
        self.stdout.write('Clearing existing data...')
        Speaker.objects.all().delete()
        CommitteeMember.objects.all().delete()
        Schedule.objects.all().delete()
        ImportantDate.objects.all().delete()
        ConferenceTrack.objects.all().delete()
        
        # Populate Keynote Speakers
        self.populate_speakers()
        
        # Populate Committee Members
        self.populate_committee()
        
        # Populate Tracks
        self.populate_tracks()
        
        # Populate Important Dates
        self.populate_important_dates()
        
        # Populate Conference Settings
        self.populate_settings()
        
        self.stdout.write(self.style.SUCCESS('Data population completed successfully!'))

    def populate_speakers(self):
        self.stdout.write('Populating Keynote Speakers...')
        
        # Get first superuser or create one
        try:
            user = User.objects.filter(is_superuser=True).first()
            if not user:
                user = User.objects.create_superuser('admin', 'admin@conference.com', 'admin')
        except:
            user = User.objects.first()
        
        speakers_data = [
            {
                'name': 'Santhakumar Sampath',
                'title': 'Research Scientist',
                'organization': 'A*STAR - Agency for Science, Technology and Research',
                'country': 'Singapore',
                'bio': 'Renowned research scientist specializing in advanced materials and manufacturing technologies with extensive publications in energy systems and intelligent manufacturing.',
                'email': 'santhakumar@astar.edu.sg',
                'linkedin': 'https://www.linkedin.com/in/santhakumar-sampath/',
                'speaker_type': 'keynote',
                'talk_title': 'Advanced Materials for Sustainable Energy Systems',
                'session_time': 'Day 1, 10:00 AM',
                'display_order': 1,
                'is_featured': True,
                'is_published': True,
                'created_by': user
            },
            {
                'name': 'JAIN A R TONY BENEDICT',
                'title': 'Professor',
                'organization': 'Gulf University',
                'country': 'Bahrain',
                'bio': 'Expert in energy systems and intelligent manufacturing with extensive research contributions in robotics, automation, and sustainable technologies.',
                'email': 'tony.benedict@gulfuniversity.edu.bh',
                'linkedin': 'https://www.linkedin.com/in/jain-a-r-tony-benedict-1a39958b/',
                'speaker_type': 'keynote',
                'talk_title': 'Intelligent Manufacturing Systems and Industry 4.0',
                'session_time': 'Day 1, 2:00 PM',
                'display_order': 2,
                'is_featured': True,
                'is_published': True,
                'created_by': user
            }
        ]
        
        for speaker_data in speakers_data:
            Speaker.objects.create(**speaker_data)
        
        self.stdout.write(self.style.SUCCESS(f'Created {len(speakers_data)} keynote speakers'))

    def populate_committee(self):
        self.stdout.write('Populating Committee Members...')
        
        committee_data = [
            # Chief Patron
            {
                'name': 'Shri Suneel Galgotia',
                'title': "Hon'ble Chancellor",
                'organization': 'Galgotias University, India',
                'email': 'chancellor@galgotiasuniversity.edu.in',
                'role': 'chief_patron',
                'hierarchy_level': 1,
                'order': 1,
                'is_active': True
            },
            # Patrons
            {
                'name': 'Dr. Dhruv Galgotia',
                'title': 'CEO',
                'organization': 'Galgotias University, India',
                'email': 'ceo@galgotiasuniversity.edu.in',
                'role': 'patron',
                'hierarchy_level': 2,
                'order': 2,
                'is_active': True
            },
            {
                'name': 'Prof. (Dr.) K.M. Babu',
                'title': 'Vice Chancellor',
                'organization': 'Galgotias University, India',
                'email': 'vc@galgotiasuniversity.edu.in',
                'role': 'patron',
                'hierarchy_level': 2,
                'order': 3,
                'is_active': True
            },
            {
                'name': 'Ms. Aradhana Galgotia',
                'title': 'Director Operations',
                'organization': 'Galgotias University, India',
                'email': 'director.operations@galgotiasuniversity.edu.in',
                'role': 'patron',
                'hierarchy_level': 2,
                'order': 4,
                'is_active': True
            },
            # Conference General Chair
            {
                'name': 'Prof. (Dr.) Avadhesh Kumar',
                'title': 'Pro-Vice Chancellor',
                'organization': 'Galgotias University, India',
                'email': 'provc@galgotiasuniversity.edu.in',
                'role': 'chair',
                'hierarchy_level': 3,
                'order': 5,
                'is_active': True
            },
            {
                'name': 'Dr. Sudhir Kumar Singh',
                'title': 'Dean Engineering',
                'organization': 'Galgotias University, India',
                'email': 'dean.engineering@galgotiasuniversity.edu.in',
                'role': 'chair',
                'hierarchy_level': 3,
                'order': 6,
                'is_active': True
            },
            {
                'name': 'Dr. P. K. S. Nain',
                'title': 'Professor',
                'organization': 'Galgotias University, India',
                'email': 'pks.nain@galgotiasuniversity.edu.in',
                'role': 'chair',
                'hierarchy_level': 3,
                'order': 7,
                'is_active': True
            },
            {
                'name': 'Dr. Kaushalendra Kumar Dubey',
                'title': 'Professor',
                'organization': 'Galgotias University, India',
                'email': 'kk.dubey@galgotiasuniversity.edu.in',
                'role': 'chair',
                'hierarchy_level': 3,
                'order': 8,
                'is_active': True
            },
            # Conveners
            {
                'name': 'Dr. R. Ashok',
                'title': 'Associate Professor',
                'organization': 'Galgotias University, India',
                'email': 'r.ashok@galgotiasuniversity.edu.in',
                'role': 'organizing_chair',
                'hierarchy_level': 6,
                'order': 9,
                'is_active': True
            },
            {
                'name': 'Dr. Pravin Kr. Singh',
                'title': 'Associate Professor',
                'organization': 'Galgotias University, India',
                'email': 'pravin.singh@galgotiasuniversity.edu.in',
                'role': 'organizing_chair',
                'hierarchy_level': 6,
                'order': 10,
                'is_active': True
            },
            # Co-Conveners
            {
                'name': 'Dr. Abhilash Purohit',
                'title': 'Assistant Professor',
                'organization': 'Galgotias University, India',
                'email': 'abhilash.purohit@galgotiasuniversity.edu.in',
                'role': 'organizing_co_chair',
                'hierarchy_level': 6,
                'order': 11,
                'is_active': True
            },
            {
                'name': 'Dr. Manav Kumar',
                'title': 'Assistant Professor',
                'organization': 'Galgotias University, India',
                'email': 'manav.kumar@galgotiasuniversity.edu.in',
                'role': 'organizing_co_chair',
                'hierarchy_level': 6,
                'order': 12,
                'is_active': True
            },
            {
                'name': 'Prof. Viveksheel Yadav',
                'title': 'Professor',
                'organization': 'Galgotias University, India',
                'email': 'viveksheel.yadav@galgotiasuniversity.edu.in',
                'role': 'organizing_co_chair',
                'hierarchy_level': 6,
                'order': 13,
                'is_active': True
            },
            # Technical Chairs
            {
                'name': 'Dr. Nav Rattan',
                'title': 'Associate Professor',
                'organization': 'Galgotias University, India',
                'email': 'nav.rattan@galgotiasuniversity.edu.in',
                'role': 'technical_chair',
                'hierarchy_level': 5,
                'order': 14,
                'is_active': True
            },
            {
                'name': 'Dr. Shrikant Vidya',
                'title': 'Associate Professor',
                'organization': 'Galgotias University, India',
                'email': 'shrikant.vidya@galgotiasuniversity.edu.in',
                'role': 'technical_chair',
                'hierarchy_level': 5,
                'order': 15,
                'is_active': True
            },
            {
                'name': 'Dr. Arun Kumar',
                'title': 'Associate Professor',
                'organization': 'Galgotias University, India',
                'email': 'arun.kumar@galgotiasuniversity.edu.in',
                'role': 'technical_chair',
                'hierarchy_level': 5,
                'order': 16,
                'is_active': True
            },
            {
                'name': 'Dr. Mayur Pratap Singh',
                'title': 'Assistant Professor',
                'organization': 'Galgotias University, India',
                'email': 'mayur.singh@galgotiasuniversity.edu.in',
                'role': 'technical_chair',
                'hierarchy_level': 5,
                'order': 17,
                'is_active': True
            },
        ]
        
        # Committee Members (without photos)
        committee_members = [
            'Dr. Abdul Gani', 'Dr. Pankaj Kumar Chauhan', 'Mr. Lavepreet Singh',
            'Dr. Ankur Gupta', 'Mr. Prabhat Kumar', 'Dr. Kamlesh Paswan',
            'Dr. Santosh Kumar Yadav', 'Mr. Abhishek Kumar Shukla', 'Dr. Tanmoy Das',
            'Dr. Nidhi', 'Mr. Md. Shazli Al Haque', 'Mr. Sandeep Kumar',
            'Dr. Ajeet Kumar', 'Mr. Anuj Kumar', 'Dr. Prabhat Kumar',
            'Dr. Pramod Kumar', 'Mr. Kapil Rajput', 'Mr. Kuldeep Narwat',
            'Mr Faisal Shameem', 'Dr. Ashish Kumar'
        ]
        
        order = 18
        for member in committee_members:
            email_name = member.lower().replace(' ', '.').replace('dr.', '').replace('mr.', '').replace('ms.', '').strip()
            committee_data.append({
                'name': member,
                'title': 'Faculty Member',
                'organization': 'Galgotias University, India',
                'email': f"{email_name}@galgotiasuniversity.edu.in",
                'role': 'member',
                'hierarchy_level': 8,
                'order': order,
                'is_active': True
            })
            order += 1
        
        for member_data in committee_data:
            CommitteeMember.objects.create(**member_data)
        
        self.stdout.write(self.style.SUCCESS(f'Created {len(committee_data)} committee members'))

    def populate_tracks(self):
        self.stdout.write('Populating Conference Tracks...')
        
        tracks_data = [
            {
                'track_number': 1,
                'title': 'Energy Systems',
                'description': 'Alternative fuels, Biogas and Biomass, Energy Storage Batteries and other Storage Devices, Fuel cell, Sustainable Hydrogen Technologies, Future Energy Technologies, Global warming & Green Energy Options, Health and Environment, Hybrid vehicles & Integration, Green Hydrogen, Energy Efficiency, Renewable Energy systems',
                'track_type': 'regular',
                'track_chair': 'Dr. R. Ashok'
            },
            {
                'track_number': 2,
                'title': 'Robotics and Automation',
                'description': 'Industrial Robots and cobots, Drones and UAVs, Autonomous Wheeled mobile Robot, Agricultural robotics, Medical Robotics, Future Energy Technologies, Defense Robotics, Service Robotics',
                'track_type': 'regular',
                'track_chair': 'Dr. Nav Rattan'
            },
            {
                'track_number': 3,
                'title': 'Intelligent Manufacturing',
                'description': 'CAD/CAM/CAE/CIM, Computational Mechanics & Techniques, Control and Automation, Flexible/Lean Manufacturing, High-Speed/Precision Machining & Inspection, Measurement Control Technologies and Intelligent Systems, Mechatronics, MEMS and Nanotechnology, Metal Cutting and forming Processes, Modeling, Analysis & Simulation of Manufacturing Processes, Non-Conventional Machining Processes, Surface Engineering, Sustainable Manufacturing Technologies, Industrial Engineering & Management',
                'track_type': 'regular',
                'track_chair': 'Dr. Shrikant Vidya'
            },
            {
                'track_number': 4,
                'title': 'Advanced Materials',
                'description': 'Advanced High strength steels, New generation materials alloys, Biomaterials, Ceramic Materials, Characterization & Testing, Composite Materials, Dynamic Behavior of Materials and Structures, Functional Materials, High temperature & Cryogenic Processing of Materials, Materials for Automotive, Energy and Environment, Nanomaterials, Smart and Device Materials, Smart Construction Materials',
                'track_type': 'regular',
                'track_chair': 'Dr. Arun Kumar'
            }
        ]
        
        for track_data in tracks_data:
            ConferenceTrack.objects.create(**track_data)
        
        self.stdout.write(self.style.SUCCESS(f'Created {len(tracks_data)} conference tracks'))

    def populate_important_dates(self):
        self.stdout.write('Populating Important Dates...')
        
        dates_data = [
            {
                'event': 'Last date for paper submission',
                'date': date(2025, 12, 31),
                'description': 'Final deadline for submitting full research papers',
                'order': 1
            },
            {
                'event': 'Notification of acceptance',
                'date': date(2026, 1, 10),
                'description': 'Authors will be notified about paper acceptance status',
                'order': 2
            },
            {
                'event': 'Registration deadline',
                'date': date(2026, 1, 31),
                'description': 'Last date for conference registration',
                'order': 3
            },
            {
                'event': 'Camera ready paper submission',
                'date': date(2026, 2, 28),
                'description': 'Final version of accepted papers must be submitted',
                'order': 4
            },
            {
                'event': 'Conference Day 1',
                'date': date(2026, 3, 17),
                'description': 'First day of ICEIMS 2026 conference',
                'order': 5
            },
            {
                'event': 'Conference Day 2',
                'date': date(2026, 3, 18),
                'description': 'Second day of ICEIMS 2026 conference',
                'order': 6
            }
        ]
        
        for date_data in dates_data:
            ImportantDate.objects.create(**date_data)
        
        self.stdout.write(self.style.SUCCESS(f'Created {len(dates_data)} important dates'))

    def populate_settings(self):
        self.stdout.write('Populating Conference Settings...')
        
        about_text = """The university began operations in the 2011-2012 academic session and welcomed its first batch of students in July 2011. Since then, it has grown to have more than 30K+ students. Today, with 20 schools offering over 200 programs, including Diploma, Undergraduate, Postgraduate, and PhD Programs, we rank among India's top universities. We aim to become an internationally recognized institution that excels in multidisciplinary and interdisciplinary education, research, and innovation, producing graduates who are globally competitive and poised to become leaders in their fields. Graduates will possess deep knowledge in their chosen fields, strong problem-solving skills, an understanding of the societal context of their profession, effective teamwork abilities, excellent communication skills, and a commitment to lifelong learning."""
        
        objectives = """The International Conference on Energy and Intelligent Manufacturing Systems aims to bring together researchers, academicians, industry experts, and policymakers to share knowledge, innovative practices, and emerging technologies in the fields of energy systems and intelligent manufacturing. The conference seeks to:

1. Promote Knowledge Exchange – Provide a platform for presenting cutting-edge research findings, case studies, and practical applications in sustainable energy and advanced manufacturing systems.

2. Foster Interdisciplinary Collaboration – Encourage interaction between experts from energy, manufacturing, automation, and artificial intelligence domains to address global industrial and environmental challenges.

3. Highlight Sustainable Practices – Explore strategies for clean energy integration, resource optimization, and environmentally responsible manufacturing.

4. Showcase Technological Innovations – Present recent advancements in smart manufacturing, Industry 4.0, robotics, digital twins, and intelligent energy management.

5. Strengthen Academia–Industry Linkages – Facilitate partnerships and collaborations between universities, research institutions, and industries for future projects and innovation.

6. Inspire Future Research – Motivate young researchers and professionals to engage in innovative work that contributes to energy efficiency, smart production systems, and sustainable industrial development."""
        
        ConferenceSettings.objects.create(
            site_title='ICEIMS 2026',
            conference_dates='March 17-18, 2026',
            location='Galgotias University, Plot No. 2, Yamuna Expressway, Greater Noida, Uttar Pradesh 201308, India',
            about_text=about_text,
            conference_objective=objectives
        )
        
        self.stdout.write(self.style.SUCCESS('Created conference settings'))
