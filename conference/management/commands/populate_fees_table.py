from django.core.management.base import BaseCommand
from conference.models import RegistrationFeesTable


class Command(BaseCommand):
    help = 'Populate sample registration fees table data'

    def handle(self, *args, **kwargs):
        self.stdout.write('🔄 Populating Registration Fees Table...')
        
        fees_data = [
            {
                'participant_type': 'indian_author',
                'display_name': 'Indian Author (Academia/Industry)',
                'early_bird_ieee': '₹6000',
                'early_bird_non_ieee': '₹7000',
                'regular_ieee': '₹7000',
                'regular_non_ieee': '₹8000',
                'display_order': 1,
                'is_highlighted': False,
                'notes': 'Maximum 2 papers per author'
            },
            {
                'participant_type': 'indian_student_author',
                'display_name': 'Indian Student Author',
                'early_bird_ieee': '₹4500',
                'early_bird_non_ieee': '₹5500',
                'regular_ieee': '₹5500',
                'regular_non_ieee': '₹6500',
                'display_order': 2,
                'is_highlighted': True,
                'notes': 'Valid student ID required'
            },
            {
                'participant_type': 'indian_attendee',
                'display_name': 'Indian Attendee (Non-Author)',
                'early_bird_ieee': '₹3000',
                'early_bird_non_ieee': '₹3500',
                'regular_ieee': '₹3500',
                'regular_non_ieee': '₹4000',
                'display_order': 3,
                'is_highlighted': False,
            },
            {
                'participant_type': 'indian_student_attendee',
                'display_name': 'Indian Student Attendee (Non-Author)',
                'early_bird_ieee': '₹2000',
                'early_bird_non_ieee': '₹2500',
                'regular_ieee': '₹2500',
                'regular_non_ieee': '₹3000',
                'display_order': 4,
                'is_highlighted': False,
                'notes': 'Valid student ID required'
            },
            {
                'participant_type': 'tutorial_indian',
                'display_name': 'Tutorial only (Indian Student)',
                'early_bird_ieee': '₹1500',
                'early_bird_non_ieee': '₹2000',
                'regular_ieee': '₹2000',
                'regular_non_ieee': '₹2500',
                'display_order': 5,
                'is_highlighted': False,
            },
            {
                'participant_type': 'foreign_author',
                'display_name': 'Foreign Author (Academia/Industry)',
                'early_bird_ieee': '$200',
                'early_bird_non_ieee': '$250',
                'regular_ieee': '$250',
                'regular_non_ieee': '$300',
                'display_order': 6,
                'is_highlighted': False,
                'notes': 'Maximum 2 papers per author'
            },
            {
                'participant_type': 'foreign_student_author',
                'display_name': 'Foreign Student Author',
                'early_bird_ieee': '$150',
                'early_bird_non_ieee': '$200',
                'regular_ieee': '$200',
                'regular_non_ieee': '$250',
                'display_order': 7,
                'is_highlighted': True,
                'notes': 'Valid student ID required'
            },
            {
                'participant_type': 'foreign_attendee',
                'display_name': 'Foreign Attendee (Non-Author)',
                'early_bird_ieee': '$100',
                'early_bird_non_ieee': '$125',
                'regular_ieee': '$125',
                'regular_non_ieee': '$150',
                'display_order': 8,
                'is_highlighted': False,
            },
            {
                'participant_type': 'foreign_student_attendee',
                'display_name': 'Foreign Student Attendee (Non-Author)',
                'early_bird_ieee': '$75',
                'early_bird_non_ieee': '$100',
                'regular_ieee': '$100',
                'regular_non_ieee': '$125',
                'display_order': 9,
                'is_highlighted': False,
                'notes': 'Valid student ID required'
            },
            {
                'participant_type': 'tutorial_foreign',
                'display_name': 'Tutorial only (Foreign Student)',
                'early_bird_ieee': '$50',
                'early_bird_non_ieee': '$75',
                'regular_ieee': '$75',
                'regular_non_ieee': '$100',
                'display_order': 10,
                'is_highlighted': False,
            },
        ]
        
        created_count = 0
        updated_count = 0
        
        for data in fees_data:
            obj, created = RegistrationFeesTable.objects.update_or_create(
                participant_type=data['participant_type'],
                defaults=data
            )
            if created:
                created_count += 1
                self.stdout.write(f'  ✅ Created: {data["display_name"]}')
            else:
                updated_count += 1
                self.stdout.write(f'  🔄 Updated: {data["display_name"]}')
        
        self.stdout.write(self.style.SUCCESS(f'\n✨ Done! Created: {created_count}, Updated: {updated_count}'))
        self.stdout.write(self.style.SUCCESS('📊 Fees table is ready to use!'))
        self.stdout.write('\n💡 You can now manage fees from: /admin/conference/registrationfeestable/')
