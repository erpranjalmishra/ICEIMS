from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from conference.models import RegistrationCategory, RegistrationSettings


class Command(BaseCommand):
    help = 'Populate initial registration categories and settings'

    def handle(self, *args, **options):
        self.stdout.write('🚀 Populating registration categories...')
        
        # Early bird deadline (example: 3 months from now)
        early_bird_deadline = (timezone.now() + timedelta(days=90)).date()
        
        # Create registration categories
        categories = [
            {
                'category_type': 'indian_author_academia',
                'display_name': 'Indian Author (Academia/Industry)',
                'currency': 'INR',
                'early_bird_ieee_member': 9500,
                'early_bird_non_ieee': 10620,
                'standard_ieee_member': 10620,
                'standard_non_ieee': 11800,
                'early_bird_deadline': early_bird_deadline,
                'display_order': 1,
                'requires_paper': True,
            },
            {
                'category_type': 'indian_student_author',
                'display_name': 'Indian Student Author',
                'currency': 'INR',
                'early_bird_ieee_member': 7080,
                'early_bird_non_ieee': 8260,
                'standard_ieee_member': 8260,
                'standard_non_ieee': 8850,
                'early_bird_deadline': early_bird_deadline,
                'display_order': 2,
                'requires_paper': True,
                'requires_student_id': True,
            },
            {
                'category_type': 'indian_student_attendee',
                'display_name': 'Indian Student Attendee (Non-Author)',
                'currency': 'INR',
                'early_bird_ieee_member': 3540,
                'early_bird_non_ieee': 4130,
                'standard_ieee_member': 4130,
                'standard_non_ieee': 4720,
                'early_bird_deadline': early_bird_deadline,
                'display_order': 3,
                'requires_student_id': True,
            },
            {
                'category_type': 'indian_professional_attendee',
                'display_name': 'Indian Professional Attendee (Non-Author)',
                'currency': 'INR',
                'early_bird_ieee_member': 5900,
                'early_bird_non_ieee': 6490,
                'standard_ieee_member': 6490,
                'standard_non_ieee': 6490,
                'early_bird_deadline': early_bird_deadline,
                'display_order': 4,
            },
            {
                'category_type': 'tutorial_indian_student',
                'display_name': 'Tutorial only (Indian Student)',
                'currency': 'INR',
                'early_bird_ieee_member': 590,
                'early_bird_non_ieee': 750,
                'standard_ieee_member': 750,
                'standard_non_ieee': 1000,
                'early_bird_deadline': early_bird_deadline,
                'display_order': 5,
                'requires_student_id': True,
            },
            {
                'category_type': 'foreign_author_academia',
                'display_name': 'Foreign Author (Academia/Industry)',
                'currency': 'USD',
                'early_bird_ieee_member': 300,
                'early_bird_non_ieee': 400,
                'standard_ieee_member': 400,
                'standard_non_ieee': 450,
                'early_bird_deadline': early_bird_deadline,
                'display_order': 6,
                'requires_paper': True,
            },
            {
                'category_type': 'foreign_student_author',
                'display_name': 'Foreign Student Author',
                'currency': 'USD',
                'early_bird_ieee_member': 150,
                'early_bird_non_ieee': 200,
                'standard_ieee_member': 200,
                'standard_non_ieee': 250,
                'early_bird_deadline': early_bird_deadline,
                'display_order': 7,
                'requires_paper': True,
                'requires_student_id': True,
            },
            {
                'category_type': 'foreign_student_attendee',
                'display_name': 'Foreign Student Attendee (Non-Author)',
                'currency': 'USD',
                'early_bird_ieee_member': 100,
                'early_bird_non_ieee': 150,
                'standard_ieee_member': 150,
                'standard_non_ieee': 200,
                'early_bird_deadline': early_bird_deadline,
                'display_order': 8,
                'requires_student_id': True,
            },
            {
                'category_type': 'foreign_professional_attendee',
                'display_name': 'Foreign Professional Attendee (Non-Author)',
                'currency': 'USD',
                'early_bird_ieee_member': 150,
                'early_bird_non_ieee': 200,
                'standard_ieee_member': 200,
                'standard_non_ieee': 250,
                'early_bird_deadline': early_bird_deadline,
                'display_order': 9,
            },
            {
                'category_type': 'tutorial_foreign_student',
                'display_name': 'Tutorial only (Foreign Student)',
                'currency': 'USD',
                'early_bird_ieee_member': 15,
                'early_bird_non_ieee': 30,
                'standard_ieee_member': 30,
                'standard_non_ieee': 50,
                'early_bird_deadline': early_bird_deadline,
                'display_order': 10,
                'requires_student_id': True,
            },
        ]
        
        created_count = 0
        updated_count = 0
        
        for cat_data in categories:
            category, created = RegistrationCategory.objects.update_or_create(
                category_type=cat_data['category_type'],
                defaults=cat_data
            )
            if created:
                created_count += 1
                self.stdout.write(self.style.SUCCESS(f'✅ Created: {category.display_name}'))
            else:
                updated_count += 1
                self.stdout.write(self.style.WARNING(f'⚠️  Updated: {category.display_name}'))
        
        # Create or update registration settings
        settings, created = RegistrationSettings.objects.get_or_create(
            pk=1,
            defaults={
                'registration_open': True,
                'early_bird_deadline': early_bird_deadline,
                'registration_message': 'Welcome to ICEIMS 2026 Registration!',
                'bank_name': 'Punjab National Bank',
                'account_name': 'GU Conferences',
                'account_number': '671700010025845',
                'ifsc_code': 'PUNB0671700',
                'swift_code': 'PUNBINBBMSN',
                'bank_address': 'Punjab National Bank, Noida',
                'pay_now_indian_link': 'https://your-payment-gateway.com/indian',
                'pay_now_international_link': 'https://your-payment-gateway.com/international',
                'important_info_title': 'Important Registration Information',
                'show_payment_buttons': True,
                'show_important_info': True,
                'show_account_details': True,
                'show_registration_process': True,
            }
        )
        
        if created:
            self.stdout.write(self.style.SUCCESS('✅ Created registration settings'))
        else:
            self.stdout.write(self.style.WARNING('⚠️  Registration settings already exist'))
        
        self.stdout.write(self.style.SUCCESS(
            f'\n🎉 Completed! Created: {created_count}, Updated: {updated_count}'
        ))
