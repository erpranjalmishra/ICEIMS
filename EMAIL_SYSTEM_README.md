# Email System Setup Guide

## Overview
This email system provides comprehensive email management with OTP-based authentication, automated emails, security notifications, and campaign management.

## Features Implemented

### ✅ Core Features
- **Gmail SMTP Integration**: Send emails via Google's SMTP server
- **OTP-Based Authentication**: 6-digit OTP codes with 10-minute expiry
- **Automated Emails**: Welcome emails, login notifications, security alerts
- **Email Templates**: 6 pre-built templates with variable substitution
- **Email Logging**: Track all sent emails with status, opens, and clicks
- **Email Campaigns**: Bulk email sending with scheduling
- **Security Event Logging**: Track and notify on security events
- **Admin Panel**: Complete interface for email management

### 📧 Email Templates Included
1. **Welcome Email** - Sent on user creation
2. **Login Notification** - Sent on successful login
3. **Security Alert** - Sent on security events
4. **OTP Verification** - Sent for OTP-based login
5. **Account Created** - Admin notification of new account
6. **Role Assignment** - Notification of role changes

## Database Models

### EmailTemplate
- Stores reusable email templates with HTML/text body
- Supports template variables ({{user_name}}, {{otp_code}}, etc.)
- 10 template types available

### EmailLog
- Tracks all sent emails with status and timestamps
- Records opens and clicks
- Links to campaigns and templates

### OTPVerification
- Stores OTP codes with expiry and verification status
- Tracks failed attempts (max 3)
- Supports resend with cooldown period

### SecurityEvent
- Logs security-related events
- 14 event types (login, password_change, role_change, etc.)
- Stores IP, user agent, and metadata

### EmailCampaign
- Bulk email sending with recipient filters
- Scheduling support
- Statistics tracking (sent, failed, opened, clicked)

## Configuration

### Environment Variables Required

Create a `.env` file in your project root with:

```env
# Email Configuration
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-specific-password
DEFAULT_FROM_EMAIL=ICEIMS 2026 <your-email@gmail.com>

# Optional: Disable emails in development
# SEND_SECURITY_EMAILS=False
# SEND_WELCOME_EMAILS=False
# SEND_LOGIN_NOTIFICATIONS=False
```

### Gmail App Password Setup

**IMPORTANT**: You cannot use your regular Gmail password. You must create an App Password.

1. Go to your Google Account: https://myaccount.google.com/
2. Select **Security** from the left menu
3. Under "How you sign in to Google," select **2-Step Verification** (enable if not already)
4. At the bottom of the page, select **App passwords**
5. Select app: **Mail**
6. Select device: **Other (Custom name)** - enter "Django ICEIMS"
7. Click **Generate**
8. Copy the 16-character password (remove spaces)
9. Use this password in `EMAIL_HOST_PASSWORD`

### Settings Already Configured

The following settings are already in `settings.py`:

```python
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD')
DEFAULT_FROM_EMAIL = os.getenv('DEFAULT_FROM_EMAIL', 'ICEIMS 2026 <noreply@iceims2026.com>')
EMAIL_TIMEOUT = 30

# OTP Settings
OTP_EXPIRY_MINUTES = 10
OTP_LENGTH = 6
MAX_OTP_ATTEMPTS = 3
OTP_RESEND_COOLDOWN = 60  # seconds

# Email Notification Toggles
SEND_SECURITY_EMAILS = True
SEND_WELCOME_EMAILS = True
SEND_LOGIN_NOTIFICATIONS = True
```

## Database Migration

Already completed! But if you need to re-run:

```bash
python manage.py makemigrations
python manage.py migrate
```

## Default Templates

Create default email templates by running:

```bash
python manage.py create_email_templates
```

This will create 6 default templates with professional HTML designs.

## Admin Panel Access

### Email Management URLs

1. **Email Templates**: `/admin-panel/emails/templates/`
   - List, create, edit, delete templates
   - Preview templates with sample data

2. **Email Logs**: `/admin-panel/emails/logs/`
   - View all sent emails
   - Filter by status, date range
   - See open/click statistics

3. **Email Campaigns**: `/admin-panel/emails/campaigns/`
   - Create and manage bulk email campaigns
   - Schedule sends or send immediately
   - Track success/failure rates

4. **Security Events**: `/admin-panel/emails/security/`
   - View security event logs
   - Filter by event type, user, date
   - See which events triggered emails

### Access Requirements
- Email Templates, Logs, Campaigns, Security Events: **Superuser only**

## Using the Email System

### Send Welcome Email

```python
from conference.email_utils import send_welcome_email

# In your user creation view
send_welcome_email(user, request)
```

### Send Login Notification

```python
from conference.email_utils import send_login_notification

# In your login view
send_login_notification(user, request)
```

### Send OTP for Login

```python
from conference.email_utils import create_and_send_otp

# Generate and send OTP
otp_instance = create_and_send_otp(
    user=user,
    purpose='login',
    method='email',
    request=request
)
```

### Verify OTP

```python
from conference.email_utils import verify_otp

# Verify user's OTP
is_valid, message, otp_instance = verify_otp(
    user=user,
    code=user_entered_code,
    purpose='login'
)

if is_valid:
    # OTP is correct, proceed with login
    pass
else:
    # Show error message
    messages.error(request, message)
```

### Log Security Events

```python
from conference.email_utils import log_security_event

# Log a security event
log_security_event(
    user=user,
    event_type='password_change',
    description='User changed their password',
    request=request,
    send_email=True  # Will send security alert email
)
```

### Send Bulk Emails

```python
from conference.email_utils import send_bulk_email
from conference.models import EmailTemplate

template = EmailTemplate.objects.get(name='Welcome Email')
recipients = ['user1@example.com', 'user2@example.com']

success_count, fail_count = send_bulk_email(
    template=template,
    recipients=recipients,
    context={'user_name': 'Admin'}
)
```

## Integration Guide

### 1. Add to User Creation View

```python
from conference.email_utils import send_welcome_email, log_security_event

@login_required
@user_passes_test(lambda u: u.is_superuser)
def user_create(request):
    if request.method == 'POST':
        # ... existing user creation code ...
        
        # Send welcome email
        if user.email:
            send_welcome_email(user, request)
        
        # Log security event
        log_security_event(
            user=request.user,
            event_type='user_created',
            description=f'Created user account: {user.username}',
            request=request,
            metadata={'new_user_id': user.id}
        )
```

### 2. Add to Login View

```python
from conference.email_utils import send_login_notification, log_security_event

def admin_login(request):
    if request.method == 'POST':
        # ... existing login code ...
        
        if user is not None:
            login(request, user)
            
            # Send login notification
            if user.email:
                send_login_notification(user, request)
            
            # Log security event
            log_security_event(
                user=user,
                event_type='login',
                description='User logged in successfully',
                request=request
            )
```

### 3. Add OTP Login (Optional)

Create new view `admin_login_otp`:

```python
from conference.email_utils import create_and_send_otp, verify_otp

def admin_login_otp_request(request):
    """Request OTP for login"""
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(username=username, password=password)
        if user:
            # Store user ID in session temporarily
            request.session['otp_user_id'] = user.id
            
            # Send OTP
            create_and_send_otp(user, 'login', 'email', request)
            messages.success(request, 'OTP sent to your email!')
            return redirect('conference:admin_login_otp_verify')
        else:
            messages.error(request, 'Invalid credentials')
    
    return render(request, 'admin/login_otp_request.html')

def admin_login_otp_verify(request):
    """Verify OTP and complete login"""
    user_id = request.session.get('otp_user_id')
    if not user_id:
        return redirect('conference:admin_login_otp_request')
    
    user = User.objects.get(id=user_id)
    
    if request.method == 'POST':
        otp_code = request.POST.get('otp_code')
        is_valid, message, otp_instance = verify_otp(user, otp_code, 'login')
        
        if is_valid:
            login(request, user)
            del request.session['otp_user_id']
            
            # Send login notification
            send_login_notification(user, request)
            log_security_event(user, 'login', 'OTP login successful', request)
            
            messages.success(request, 'Login successful!')
            return redirect('conference:admin_dashboard')
        else:
            messages.error(request, message)
    
    return render(request, 'admin/login_otp_verify.html', {'user': user})
```

## Testing

### Test Email Sending

```bash
python manage.py shell
```

```python
from django.contrib.auth.models import User
from conference.email_utils import send_welcome_email

# Get a user
user = User.objects.first()

# Test sending welcome email
send_welcome_email(user, None)

# Check email logs
from conference.models import EmailLog
EmailLog.objects.all()
```

### Test OTP Generation

```python
from conference.email_utils import create_and_send_otp, verify_otp

user = User.objects.first()

# Create and send OTP
otp = create_and_send_otp(user, 'login', 'email', None)
print(f"OTP Code: {otp.code}")  # For testing

# Verify OTP
is_valid, message, otp_instance = verify_otp(user, otp.code, 'login')
print(f"Valid: {is_valid}, Message: {message}")
```

## Troubleshooting

### Emails Not Sending

1. **Check Gmail App Password**:
   - Must use App Password, not regular password
   - Ensure 2-Step Verification is enabled

2. **Check Environment Variables**:
   ```bash
   python manage.py shell
   ```
   ```python
   import os
   print(os.getenv('EMAIL_HOST_USER'))
   print(os.getenv('EMAIL_HOST_PASSWORD'))
   ```

3. **Check Email Logs**:
   - Go to `/admin-panel/emails/logs/`
   - Look for error messages

4. **Test SMTP Connection**:
   ```python
   from django.core.mail import send_mail
   
   send_mail(
       'Test Subject',
       'Test message',
       os.getenv('EMAIL_HOST_USER'),
       ['recipient@example.com'],
       fail_silently=False,
   )
   ```

### OTP Not Working

1. **Check OTP Expiry**: Default is 10 minutes
2. **Check Attempts**: Max 3 attempts allowed
3. **Check Resend Cooldown**: 60 seconds between resends

### Security Events Not Logging

1. **Check Settings**:
   - `SEND_SECURITY_EMAILS = True`
2. **Check Email Template**: Security Alert template must exist
3. **Check User Email**: User must have email address

## File Structure

```
conference/
├── models.py                      # Email models
├── email_utils.py                 # Email utility functions
├── views.py                       # Email admin views (added at end)
├── urls.py                        # Email URLs (added at end)
├── management/
│   └── commands/
│       └── create_email_templates.py  # Create default templates
└── migrations/
    └── 0022_add_email_and_otp_models.py

templates/admin/
├── email_template_list.html      # List email templates
├── email_template_form.html      # Create/edit template
├── email_template_confirm_delete.html
├── email_log_list.html           # View email logs
├── email_campaign_list.html      # List campaigns
├── email_campaign_form.html      # Create campaign
├── email_campaign_confirm_send.html
└── security_event_list.html      # View security events
```

## Next Steps

1. ✅ **Setup Complete** - All models, views, URLs created
2. ⏳ **Add Environment Variables** - Create `.env` file with Gmail credentials
3. ⏳ **Create Templates** - Run `python manage.py create_email_templates`
4. ⏳ **Integrate with Existing Views** - Add email sending to user creation/login
5. ⏳ **Create OTP Login Views** - Optional OTP-based authentication
6. ⏳ **Test Email Sending** - Send test emails
7. ⏳ **Create Remaining Templates** - Add templates for campaigns, etc.

## Security Notes

- **Never commit `.env` file** - Add to `.gitignore`
- **Use App Passwords only** - Never use your main Gmail password
- **Enable 2FA on Gmail** - Required for App Passwords
- **Limit OTP attempts** - Max 3 attempts, then lockout
- **Monitor security events** - Check `/admin-panel/emails/security/` regularly
- **Validate email addresses** - Ensure user emails are valid before sending

## Support

For issues or questions:
1. Check email logs at `/admin-panel/emails/logs/`
2. Check security events at `/admin-panel/emails/security/`
3. Review this documentation
4. Check Django error logs

---

**Created**: December 2024  
**Status**: ✅ Database & Backend Complete | ⏳ Frontend Templates Pending  
**Version**: 1.0
