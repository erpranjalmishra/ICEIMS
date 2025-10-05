"""
Management command to clear all caches
"""
from django.core.management.base import BaseCommand
from django.core.cache import cache


class Command(BaseCommand):
    help = 'Clear all Django caches'

    def handle(self, *args, **options):
        self.stdout.write(self.style.WARNING('Clearing all caches...'))
        
        try:
            cache.clear()
            self.stdout.write(self.style.SUCCESS('✓ Cache cleared successfully!'))
            
            # Additional cleanup
            from django.core.cache import caches
            for cache_name in caches:
                caches[cache_name].clear()
                self.stdout.write(self.style.SUCCESS(f'✓ Cleared cache: {cache_name}'))
                
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'✗ Error clearing cache: {str(e)}'))
            
        self.stdout.write(self.style.SUCCESS('\nCache clearing complete!'))
