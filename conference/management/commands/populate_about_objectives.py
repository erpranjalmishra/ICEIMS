from django.core.management.base import BaseCommand
from conference.models import AboutObjective


class Command(BaseCommand):
    help = 'Populate default conference objectives for about page'

    def handle(self, *args, **kwargs):
        objectives_data = [
            {
                'title': 'Foster Innovation',
                'description': 'Encourage innovative research and development in energy and manufacturing systems through collaborative discussions and knowledge sharing.',
                'icon': 'fas fa-lightbulb',
                'color': 'primary',
                'order': 1
            },
            {
                'title': 'Build Networks',
                'description': 'Create networking opportunities between academia and industry professionals to facilitate partnerships and collaborative research.',
                'icon': 'fas fa-users',
                'color': 'success',
                'order': 2
            },
            {
                'title': 'Promote Sustainability',
                'description': 'Advance sustainable manufacturing practices and renewable energy solutions for a greener future.',
                'icon': 'fas fa-leaf',
                'color': 'warning',
                'order': 3
            },
            {
                'title': 'Global Perspective',
                'description': 'Bring together international experts to share diverse perspectives and best practices from around the world.',
                'icon': 'fas fa-globe',
                'color': 'info',
                'order': 4
            },
        ]

        created_count = 0
        updated_count = 0

        for obj_data in objectives_data:
            objective, created = AboutObjective.objects.update_or_create(
                title=obj_data['title'],
                defaults={
                    'description': obj_data['description'],
                    'icon': obj_data['icon'],
                    'color': obj_data['color'],
                    'order': obj_data['order'],
                    'is_active': True
                }
            )
            
            if created:
                created_count += 1
                self.stdout.write(self.style.SUCCESS(f'Created: {objective.title}'))
            else:
                updated_count += 1
                self.stdout.write(self.style.WARNING(f'Updated: {objective.title}'))

        self.stdout.write(self.style.SUCCESS(
            f'\nCompleted! Created: {created_count}, Updated: {updated_count}'
        ))
