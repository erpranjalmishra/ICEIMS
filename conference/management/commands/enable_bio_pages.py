from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from conference.models import Speaker, CommitteeMember


class Command(BaseCommand):
    help = 'Update existing speakers and committee members with bio page data'

    def handle(self, *args, **options):
        self.stdout.write('🔄 Updating existing records for bio pages...\n')
        
        # Get or create a user for created_by field
        user, created = User.objects.get_or_create(
            username='admin',
            defaults={'is_staff': True, 'is_superuser': True}
        )
        
        # Update speakers
        speakers_updated = 0
        for speaker in Speaker.objects.all():
            if not speaker.created_by_id:
                speaker.created_by = user
            speaker.enable_bio_page = True
            speaker.save()
            speakers_updated += 1
            self.stdout.write(f'  ✓ Updated speaker: {speaker.name}')
        
        # Update committee members
        committee_updated = 0
        for member in CommitteeMember.objects.all():
            member.enable_bio_page = True
            member.save()
            committee_updated += 1
            self.stdout.write(f'  ✓ Updated committee member: {member.name}')
        
        self.stdout.write(self.style.SUCCESS(f'\n✨ Done!'))
        self.stdout.write(self.style.SUCCESS(f'Speakers updated: {speakers_updated}'))
        self.stdout.write(self.style.SUCCESS(f'Committee members updated: {committee_updated}'))
        self.stdout.write(self.style.SUCCESS('\n📊 Bio pages are now enabled for all records!'))
