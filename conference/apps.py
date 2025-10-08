from django.apps import AppConfig


class ConferenceConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'conference'
    
    def ready(self):
        """Import signal handlers when app is ready"""
        import conference.signals
