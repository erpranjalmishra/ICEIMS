"""
Email utility functions for the conference application
"""
from django.core.mail import send_mail, EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings
from django.utils import timezone
from datetime import timedelta
import random
import string
from .models import EmailTemplate, EmailLog, OTPVerification, SecurityEvent


def generate_otp(length=6):
    """Generate a random OTP code"""
    return ''.join(random.choices(string.digits, k=length))


def send_email_with_template(template_type, recipient_email, context, user=None):
    """
    Send email using a predefined template
    
    Args:
        template_type: Type of template to use
        recipient_email: Recipient's email address
        context: Dictionary of template variables
        user: User object if applicable
    """
    try:
        # Get the template
        template = EmailTemplate.objects.filter(
            template_type=template_type,
            is_active=True
        ).first()
        
        if not template:
            print(f"No active template found for type: {template_type}")
            return False
        
        # Add default context
        context.update({
            'site_name': 'ICEIMS 2026',
            'site_url': settings.ALLOWED_HOSTS[0] if settings.ALLOWED_HOSTS else 'localhost',
            'support_email': settings.DEFAULT_FROM_EMAIL,
        })
        
        # Render subject and body
        subject = template.subject
        for key, value in context.items():
            subject = subject.replace(f'{{{{{key}}}}}', str(value))
        
        html_body = template.body_html
        for key, value in context.items():
            html_body = html_body.replace(f'{{{{{key}}}}}', str(value))
        
        text_body = template.body_text or strip_tags(html_body)
        
        # Create email log
        email_log = EmailLog.objects.create(
            recipient=recipient_email,
            recipient_user=user,
            subject=subject,
            body=html_body,
            template=template,
            status='pending'
        )
        
        # Send email
        email = EmailMultiAlternatives(
            subject=subject,
            body=text_body,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[recipient_email]
        )
        email.attach_alternative(html_body, "text/html")
        email.send()
        
        # Update log
        email_log.status = 'sent'
        email_log.sent_at = timezone.now()
        email_log.save()
        
        return True
        
    except Exception as e:
        print(f"Error sending email: {str(e)}")
        if 'email_log' in locals():
            email_log.status = 'failed'
            email_log.error_message = str(e)
            email_log.save()
        return False


def send_welcome_email(user):
    """Send welcome email to new user"""
    if not settings.SEND_WELCOME_EMAILS:
        return False
    
    context = {
        'user_name': user.get_full_name() or user.username,
        'username': user.username,
        'email': user.email,
        'login_url': f"{settings.ALLOWED_HOSTS[0]}/admin-login/",
    }
    
    return send_email_with_template('welcome', user.email, context, user)


def send_login_notification(user, ip_address, user_agent, location=''):
    """Send login notification email"""
    if not settings.SEND_LOGIN_NOTIFICATIONS:
        return False
    
    context = {
        'user_name': user.get_full_name() or user.username,
        'email': user.email,
        'login_time': timezone.now().strftime('%Y-%m-%d %H:%M:%S'),
        'ip_address': ip_address,
        'user_agent': user_agent,
        'location': location or 'Unknown',
    }
    
    return send_email_with_template('login_notification', user.email, context, user)


def send_security_alert(user, event_type, description, ip_address):
    """Send security alert email"""
    if not settings.SEND_SECURITY_EMAILS:
        return False
    
    context = {
        'user_name': user.get_full_name() or user.username,
        'email': user.email,
        'event_type': event_type,
        'description': description,
        'time': timezone.now().strftime('%Y-%m-%d %H:%M:%S'),
        'ip_address': ip_address,
    }
    
    return send_email_with_template('security_alert', user.email, context, user)


def send_otp_email(user, otp_code, purpose='login', ip_address=None):
    """Send OTP verification email"""
    context = {
        'user_name': user.get_full_name() or user.username,
        'email': user.email,
        'otp_code': otp_code,
        'purpose': purpose,
        'expiry_minutes': settings.OTP_EXPIRY_MINUTES,
        'ip_address': ip_address or 'Unknown',
    }
    
    return send_email_with_template('otp_verification', user.email, context, user)


def create_and_send_otp(user, purpose='login', ip_address=None):
    """Create OTP and send via email"""
    # Invalidate old OTPs
    OTPVerification.objects.filter(
        user=user,
        purpose=purpose,
        is_used=False
    ).update(is_used=True)
    
    # Generate new OTP
    otp_code = generate_otp(settings.OTP_LENGTH)
    expires_at = timezone.now() + timedelta(minutes=settings.OTP_EXPIRY_MINUTES)
    
    # Create OTP record
    otp = OTPVerification.objects.create(
        user=user,
        otp_code=otp_code,
        purpose=purpose,
        expires_at=expires_at,
        ip_address=ip_address,
        max_attempts=settings.MAX_OTP_ATTEMPTS
    )
    
    # Send email
    if send_otp_email(user, otp_code, purpose, ip_address):
        # Log security event
        SecurityEvent.objects.create(
            user=user,
            event_type='otp_sent',
            description=f'OTP sent for {purpose}',
            ip_address=ip_address or '127.0.0.1',
            email_sent=True,
            email_sent_at=timezone.now()
        )
        return otp
    
    return None


def verify_otp(user, otp_code, purpose='login'):
    """Verify OTP code"""
    try:
        otp = OTPVerification.objects.filter(
            user=user,
            purpose=purpose,
            is_used=False
        ).order_by('-created_at').first()
        
        if not otp:
            return False, "No OTP found"
        
        if not otp.is_valid():
            return False, "OTP expired or max attempts exceeded"
        
        if otp.verify(otp_code):
            # Log successful verification
            SecurityEvent.objects.create(
                user=user,
                event_type='otp_verified',
                description=f'OTP verified for {purpose}',
                ip_address='127.0.0.1'
            )
            return True, "OTP verified successfully"
        else:
            # Log failed attempt
            SecurityEvent.objects.create(
                user=user,
                event_type='otp_failed',
                description=f'Failed OTP verification for {purpose}',
                ip_address='127.0.0.1'
            )
            return False, f"Invalid OTP. {otp.max_attempts - otp.attempts} attempts remaining"
            
    except Exception as e:
        return False, str(e)


def log_security_event(user, event_type, description, ip_address, user_agent='', send_email=True):
    """Log security event and optionally send notification"""
    event = SecurityEvent.objects.create(
        user=user,
        event_type=event_type,
        description=description,
        ip_address=ip_address,
        user_agent=user_agent
    )
    
    if send_email and settings.SEND_SECURITY_EMAILS:
        if send_security_alert(user, event_type, description, ip_address):
            event.email_sent = True
            event.email_sent_at = timezone.now()
            event.save()
    
    return event


def send_bulk_email(subject, message, recipient_list, html_message=None):
    """Send email to multiple recipients"""
    logs = []
    
    for recipient in recipient_list:
        try:
            email_log = EmailLog.objects.create(
                recipient=recipient,
                subject=subject,
                body=html_message or message,
                status='pending'
            )
            
            if html_message:
                email = EmailMultiAlternatives(
                    subject=subject,
                    body=message,
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    to=[recipient]
                )
                email.attach_alternative(html_message, "text/html")
                email.send()
            else:
                send_mail(
                    subject=subject,
                    message=message,
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[recipient],
                    fail_silently=False
                )
            
            email_log.status = 'sent'
            email_log.sent_at = timezone.now()
            email_log.save()
            logs.append(email_log)
            
        except Exception as e:
            email_log.status = 'failed'
            email_log.error_message = str(e)
            email_log.save()
            logs.append(email_log)
    
    return logs


def get_client_ip(request):
    """Get client IP address from request"""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR', '127.0.0.1')
    return ip


def send_role_assignment_email(user, role):
    """Send email when role is assigned to user"""
    context = {
        'user_name': user.get_full_name() or user.username,
        'email': user.email,
        'role_name': role.name if role else 'No Role',
        'role_description': role.description if role else '',
    }
    
    return send_email_with_template('role_assigned', user.email, context, user)


def send_permission_change_email(user, changes):
    """Send email when permissions are changed"""
    context = {
        'user_name': user.get_full_name() or user.username,
        'email': user.email,
        'changes': changes,
        'time': timezone.now().strftime('%Y-%m-%d %H:%M:%S'),
    }
    
    return send_email_with_template('permission_changed', user.email, context, user)
