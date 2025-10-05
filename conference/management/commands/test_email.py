"""
Management command to test email configuration
"""
from django.core.management.base import BaseCommand
from django.core.mail import send_mail
from django.conf import settings


class Command(BaseCommand):
    help = 'Test email configuration'

    def add_arguments(self, parser):
        parser.add_argument(
            '--to',
            type=str,
            help='Email address to send test email to',
            default='test@example.com'
        )

    def handle(self, *args, **options):
        to_email = options['to']
        
        self.stdout.write(self.style.WARNING('=' * 70))
        self.stdout.write(self.style.WARNING('Email Configuration Test'))
        self.stdout.write(self.style.WARNING('=' * 70))
        
        # Check settings
        self.stdout.write(f'\n{self.style.SUCCESS("✓")} Email Backend: {settings.EMAIL_BACKEND}')
        self.stdout.write(f'{self.style.SUCCESS("✓")} Email Host: {settings.EMAIL_HOST}')
        self.stdout.write(f'{self.style.SUCCESS("✓")} Email Port: {settings.EMAIL_PORT}')
        self.stdout.write(f'{self.style.SUCCESS("✓")} Use TLS: {settings.EMAIL_USE_TLS}')
        self.stdout.write(f'{self.style.SUCCESS("✓")} Email Host User: {settings.EMAIL_HOST_USER}')
        
        # Check if credentials are set
        if settings.EMAIL_HOST_USER == 'your-email@gmail.com':
            self.stdout.write(f'\n{self.style.ERROR("✗")} EMAIL_HOST_USER is not configured!')
            self.stdout.write(self.style.WARNING('  Set EMAIL_HOST_USER environment variable'))
        
        if settings.EMAIL_HOST_PASSWORD == 'your-app-password':
            self.stdout.write(f'{self.style.ERROR("✗")} EMAIL_HOST_PASSWORD is not configured!')
            self.stdout.write(self.style.WARNING('  Set EMAIL_HOST_PASSWORD environment variable'))
            self.stdout.write(self.style.WARNING('  For Gmail: Use App Password from https://myaccount.google.com/apppasswords'))
        
        # Try sending test email
        self.stdout.write(f'\n{self.style.WARNING("Testing email send to:")} {to_email}')
        
        try:
            send_mail(
                subject='Test Email from ICEIMS Conference',
                message='This is a test email to verify your email configuration is working correctly.',
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[to_email],
                fail_silently=False,
            )
            self.stdout.write(f'{self.style.SUCCESS("✓ Email sent successfully!")}')
            
        except Exception as e:
            self.stdout.write(f'{self.style.ERROR("✗ Email sending failed!")}')
            self.stdout.write(f'{self.style.ERROR(f"Error: {str(e)}")}')
            
            # Common issues
            self.stdout.write(f'\n{self.style.WARNING("Common Issues:")}')
            self.stdout.write('  1. Gmail: Enable "Less secure app access" or use App Password')
            self.stdout.write('  2. Check if EMAIL_HOST_USER and EMAIL_HOST_PASSWORD are correct')
            self.stdout.write('  3. Verify EMAIL_PORT (587 for TLS, 465 for SSL)')
            self.stdout.write('  4. Check firewall/network settings')
            
        self.stdout.write('\n' + '=' * 70 + '\n')
