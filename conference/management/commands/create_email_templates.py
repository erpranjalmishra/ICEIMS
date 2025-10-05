"""
Management command to create professional email templates with ICEIMS website branding
"""
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from conference.models import EmailTemplate


class Command(BaseCommand):
    help = 'Create professional email templates with ICEIMS branding'

    def handle(self, *args, **options):
        # Get or create a superuser for created_by
        superuser = User.objects.filter(is_superuser=True).first()
        
        # Read the actual ICEIMS logo from static files
        from pathlib import Path
        import os
        from django.conf import settings
        
        # Get the actual ICEIMS logo SVG
        logo_path = os.path.join(settings.BASE_DIR, 'static', 'images', 'ICEIMS.svg')
        try:
            with open(logo_path, 'r', encoding='utf-8') as f:
                logo_svg_full = f.read()
            # Scale it down for email and add style for proper display
            logo_svg = logo_svg_full.replace('width="2048"', 'width="200"').replace('height="675"', 'height="66"').replace('<svg', '<svg style="display:block;margin:0 auto"')
            self.stdout.write(self.style.SUCCESS('✅ Loaded actual ICEIMS logo from static/images/ICEIMS.svg'))
        except Exception as e:
            # Fallback to simple logo if file not found
            self.stdout.write(self.style.WARNING(f'⚠️  Could not load ICEIMS logo: {e}. Using fallback logo.'))
            logo_svg = '''<svg width="80" height="80" viewBox="0 0 200 200" xmlns="http://www.w3.org/2000/svg">
            <defs>
                <linearGradient id="iceims-gradient" x1="0%" y1="0%" x2="100%" y2="100%">
                    <stop offset="0%" style="stop-color:#a0352f;stop-opacity:1" />
                    <stop offset="100%" style="stop-color:#e56d2d;stop-opacity:1" />
                </linearGradient>
            </defs>
            <circle cx="100" cy="100" r="95" fill="url(#iceims-gradient)" />
            <text x="100" y="110" font-family="Arial, sans-serif" font-size="80" font-weight="bold" fill="white" text-anchor="middle">IC</text>
            <circle cx="100" cy="100" r="95" fill="none" stroke="white" stroke-width="3" opacity="0.3"/>
        </svg>'''
        
        # Common professional email styling matching website theme
        email_styles = '''
        <style>
            * { margin: 0; padding: 0; box-sizing: border-box; }
            body {
                margin: 0;
                padding: 0;
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
                background-color: #f8f9fa;
                line-height: 1.6;
                color: #212529;
            }
            .email-wrapper {
                background-color: #f8f9fa;
                padding: 20px 10px;
            }
            .email-container {
                max-width: 650px;
                margin: 0 auto;
                background-color: #ffffff;
                border-radius: 12px;
                overflow: hidden;
                box-shadow: 0 8px 32px rgba(160, 53, 47, 0.12);
                border: 1px solid rgba(160, 53, 47, 0.08);
            }
            .logo-section {
                background: #ffffff;
                padding: 30px 20px;
                text-align: center;
                border-bottom: 3px solid;
                border-image: linear-gradient(135deg, #a0352f 0%, #e56d2d 100%) 1;
            }
            .logo-img {
                width: 80px;
                height: 80px;
                margin-bottom: 12px;
            }
            .conference-title {
                color: #a0352f;
                font-size: 26px;
                font-weight: 700;
                margin: 8px 0 8px 0;
                letter-spacing: 1.5px;
            }
            .conference-subtitle {
                color: #6c757d;
                font-size: 11px;
                margin: 0;
                text-transform: uppercase;
                letter-spacing: 2px;
                font-weight: 600;
                line-height: 1.4;
            }
            .header {
                background: linear-gradient(135deg, #a0352f 0%, #e56d2d 100%);
                color: #ffffff;
                padding: 38px 30px;
                text-align: center;
                position: relative;
            }
            .header::before {
                content: '';
                position: absolute;
                top: 0;
                left: 0;
                right: 0;
                bottom: 0;
                background-image: radial-gradient(circle, rgba(255,255,255,0.1) 1px, transparent 1px);
                background-size: 20px 20px;
                opacity: 0.3;
            }
            .header h1 {
                margin: 0 0 10px 0;
                font-size: 30px;
                font-weight: 700;
                position: relative;
                z-index: 1;
                text-shadow: 0 2px 4px rgba(0,0,0,0.2);
            }
            .header p {
                margin: 0;
                font-size: 14px;
                opacity: 0.95;
                position: relative;
                z-index: 1;
                font-weight: 400;
            }
            .content {
                padding: 40px 35px;
                color: #212529;
            }
            .content h2 {
                color: #a0352f;
                font-size: 22px;
                margin: 0 0 20px 0;
                font-weight: 600;
            }
            .content p {
                margin: 15px 0;
                line-height: 1.7;
                color: #212529;
            }
            .content ul {
                margin: 15px 0;
                padding-left: 25px;
                color: #212529;
            }
            .content li {
                margin: 8px 0;
                line-height: 1.6;
            }
            .info-box {
                background: linear-gradient(135deg, #fff5f3 0%, #fef8f6 100%);
                border-left: 4px solid #a0352f;
                padding: 24px;
                margin: 28px 0;
                border-radius: 8px;
                box-shadow: 0 2px 8px rgba(160, 53, 47, 0.08);
            }
            .info-box p {
                margin: 10px 0;
                font-size: 15px;
                line-height: 1.7;
            }
            .info-box strong {
                color: #a0352f;
                min-width: 140px;
                display: inline-block;
                font-weight: 600;
            }
            .button {
                display: inline-block;
                background: linear-gradient(135deg, #a0352f 0%, #e56d2d 100%);
                color: #ffffff !important;
                padding: 16px 42px;
                text-decoration: none;
                border-radius: 8px;
                font-weight: 600;
                font-size: 15px;
                margin: 25px 0;
                box-shadow: 0 4px 16px rgba(160, 53, 47, 0.3);
                transition: all 0.3s ease;
                text-transform: uppercase;
                letter-spacing: 0.5px;
            }
            .divider {
                height: 2px;
                background: linear-gradient(to right, transparent, rgba(160, 53, 47, 0.2), transparent);
                margin: 30px 0;
            }
            .footer {
                background: linear-gradient(135deg, #a0352f 0%, #e56d2d 100%);
                color: #ffffff;
                padding: 38px 32px;
                text-align: center;
                font-size: 13px;
            }
            .footer p {
                margin: 8px 0;
                line-height: 1.6;
            }
            .footer-logo {
                font-size: 24px;
                font-weight: 700;
                color: #ffffff;
                margin-bottom: 12px;
                letter-spacing: 1.5px;
            }
            .conference-details {
                background-color: rgba(52, 73, 94, 0.5);
                padding: 24px;
                margin: 20px 0;
                border-radius: 8px;
                border: 1px solid rgba(255, 255, 255, 0.1);
            }
            .conference-details p {
                margin: 10px 0;
                font-size: 13px;
                line-height: 1.7;
            }
            .conference-details strong {
                color: #e56d2d;
            }
            .contact-info {
                margin-top: 22px;
                padding-top: 22px;
                border-top: 2px solid rgba(255, 255, 255, 0.15);
            }
            .contact-link {
                color: #e56d2d;
                text-decoration: none;
                font-weight: 600;
            }
            .disclaimer {
                margin-top: 25px;
                padding-top: 20px;
                border-top: 1px solid rgba(255, 255, 255, 0.1);
                color: #95a5a6;
                font-size: 11px;
                line-height: 1.6;
            }
        </style>
        '''
        
        templates = [
            {
                'name': 'Welcome Email',
                'template_type': 'welcome',
                'subject': 'Welcome to ICEIMS 2026 - {{user_name}}',
                'body_html': f'''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Welcome to ICEIMS 2026</title>
    {email_styles}
</head>
<body>
    <div class="email-wrapper">
        <div class="email-container">
            <div class="logo-section">
                {logo_svg}
                <div class="conference-title">ICEIMS 2026</div>
                <p class="conference-subtitle">International Conference on<br>Emerging & Intelligent Management Systems</p>
            </div>
            
            <div class="header">
                <h1>🎉 Welcome Aboard!</h1>
                <p>Your admin account has been successfully created</p>
            </div>
            
            <div class="content">
                <h2>Hello {{{{user_name}}}},</h2>
                <p>We're delighted to welcome you to the <strong>ICEIMS 2026</strong> conference management platform! Your administrator account has been successfully created, granting you access to our comprehensive management system.</p>
                
                <div class="info-box">
                    <p><strong>Email Address:</strong> {{{{email}}}}</p>
                    <p><strong>Username:</strong> {{{{username}}}}</p>
                    <p><strong>Access Level:</strong> Administrator</p>
                </div>
                
                <p>You can now log in to access the admin panel and begin managing all aspects of the conference including content, submissions, registrations, and communications.</p>
                
                <center>
                    <a href="{{{{login_url}}}}" class="button">Access Admin Panel</a>
                </center>
                
                <div class="divider"></div>
                
                <p><strong>Your Administrative Capabilities:</strong></p>
                <ul>
                    <li>Manage committee members and keynote speakers</li>
                    <li>Update conference schedule and track information</li>
                    <li>Review and publish blog posts and announcements</li>
                    <li>Monitor participant registrations and paper submissions</li>
                    <li>Send email campaigns and notifications to attendees</li>
                </ul>
                
                <p>Our support team is available 24/7 to assist you. Don't hesitate to reach out if you have any questions!</p>
            </div>
            
            <div class="footer">
                <div class="footer-logo">ICEIMS 2026</div>
                <p><strong>International Conference on Emerging & Intelligent Management Systems</strong></p>
                
                <div class="conference-details">
                    <p><strong>📅 Conference:</strong> ICEIMS 2026</p>
                    <p><strong>📍 Location:</strong> India</p>
                    <p><strong>🏛️ Organized By:</strong> Team Vimarsh</p>
                </div>
                
                <div class="contact-info">
                    <p>📧 <strong>Email:</strong> <a href="mailto:iceims.official@gmail.com" class="contact-link">iceims.official@gmail.com</a></p>
                    <p>🌐 <strong>Website:</strong> <a href="https://iceims2026.com" class="contact-link">www.iceims2026.com</a></p>
                    <p>📞 <strong>Support:</strong> Available 24/7 via email</p>
                </div>
                
                <div class="disclaimer">
                    This is an automated message from ICEIMS 2026. Please do not reply directly to this email.<br>
                    For support and inquiries, contact: <a href="mailto:iceims.official@gmail.com" class="contact-link">iceims.official@gmail.com</a>
                </div>
            </div>
        </div>
    </div>
</body>
</html>
                ''',
                'body_text': '''Welcome to ICEIMS 2026!

International Conference on Emerging & Intelligent Management Systems

Hello {{user_name}},

Your administrator account has been successfully created!

Account Details:
- Email: {{email}}
- Username: {{username}}
- Access Level: Administrator

Login URL: {{login_url}}

Conference Information:
- Email: iceims.official@gmail.com
- Website: www.iceims2026.com
- Organized by Team Vimarsh, India
- Support: Available 24/7

For assistance, contact: iceims.official@gmail.com

Best regards,
ICEIMS 2026 Team''',
            },
            {
                'name': 'Login Notification',
                'template_type': 'login_notification',
                'subject': 'New Login to Your ICEIMS Account - {{user_name}}',
                'body_html': f'''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Login Notification</title>
    {email_styles}
    <style>
        .login-header {{
            background: linear-gradient(135deg, #27ae60 0%, #229954 100%);
        }}
    </style>
</head>
<body>
    <div class="email-wrapper">
        <div class="email-container">
            <div class="logo-section">
                {logo_svg}
                <div class="conference-title">ICEIMS 2026</div>
                <p class="conference-subtitle">International Conference on<br>Emerging & Intelligent Management Systems</p>
            </div>
            
            <div class="header login-header">
                <h1>🔐 New Login Detected</h1>
                <p>Security notification for your account</p>
            </div>
            
            <div class="content">
                <h2 style="color: #27ae60;">Hello {{{{user_name}}}},</h2>
                <p>We detected a new login to your ICEIMS 2026 administrator account. For your security, we're notifying you of this access.</p>
                
                <div class="info-box" style="background: linear-gradient(135deg, #f0fdf4 0%, #ecfdf5 100%); border-left-color: #27ae60;">
                    <p><strong>Login Time:</strong> {{{{login_time}}}}</p>
                    <p><strong>IP Address:</strong> {{{{ip_address}}}}</p>
                    <p><strong>Device/Browser:</strong> {{{{user_agent}}}}</p>
                    <p><strong>Location:</strong> {{{{location}}}}</p>
                </div>
                
                <div class="info-box" style="background: linear-gradient(135deg, #fffbeb 0%, #fef3c7 100%); border-left-color: #f59e0b;">
                    <p style="margin: 0 0 12px 0;"><strong style="color: #b45309;">⚠️ Wasn't you?</strong></p>
                    <p style="color: #78350f; margin: 0;">If you did not perform this login, take immediate action:</p>
                    <ul style="margin: 12px 0 0 20px; padding: 0; color: #78350f;">
                        <li>Change your password immediately</li>
                        <li>Contact support at iceims.official@gmail.com</li>
                        <li>Review your recent account activity</li>
                    </ul>
                </div>
                
                <div class="divider"></div>
                
                <p><strong style="color: #27ae60;">🛡️ Security Best Practices:</strong></p>
                <ul>
                    <li>Use a strong, unique password (minimum 12 characters)</li>
                    <li>Enable OTP two-factor authentication</li>
                    <li>Never share your login credentials with anyone</li>
                    <li>Always log out after completing your session</li>
                    <li>Keep your browser and operating system updated</li>
                </ul>
            </div>
            
            <div class="footer">
                <div class="footer-logo">ICEIMS 2026</div>
                <p><strong>International Conference on Emerging & Intelligent Management Systems</strong></p>
                
                <div class="conference-details">
                    <p><strong>🏛️ Organized By:</strong> Team Vimarsh, India</p>
                    <p><strong>🔒 Security:</strong> We continuously monitor your account for suspicious activity</p>
                </div>
                
                <div class="contact-info">
                    <p>📧 <strong>Support:</strong> <a href="mailto:iceims.official@gmail.com" class="contact-link">iceims.official@gmail.com</a></p>
                    <p>🌐 <strong>Website:</strong> <a href="https://iceims2026.com" class="contact-link">www.iceims2026.com</a></p>
                </div>
                
                <div class="disclaimer">
                    This is an automated security notification from ICEIMS 2026.<br>
                    For immediate assistance: <a href="mailto:iceims.official@gmail.com" class="contact-link">iceims.official@gmail.com</a>
                </div>
            </div>
        </div>
    </div>
</body>
</html>
                ''',
                'body_text': '''New Login Detected - ICEIMS 2026

Hello {{user_name}},

We detected a new login to your account:

Login Details:
- Time: {{login_time}}
- IP Address: {{ip_address}}
- Device: {{user_agent}}
- Location: {{location}}

If this wasn't you, contact us immediately at iceims.official@gmail.com

Conference Information:
- Email: iceims.official@gmail.com
- Website: www.iceims2026.com
- Organized by Team Vimarsh, India

Best regards,
ICEIMS 2026 Security Team''',
            },
            {
                'name': 'Security Alert',
                'template_type': 'security_alert',
                'subject': '🔒 Security Alert - {{event_type}} - ICEIMS',
                'body_html': f'''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Security Alert</title>
    {email_styles}
    <style>
        .alert-header {{
            background: linear-gradient(135deg, #dc2626 0%, #ef4444 100%);
        }}
    </style>
</head>
<body>
    <div class="email-wrapper">
        <div class="email-container">
            <div class="logo-section">
                {logo_svg}
                <div class="conference-title">ICEIMS 2026</div>
                <p class="conference-subtitle">International Conference on<br>Emerging & Intelligent Management Systems</p>
            </div>
            
            <div class="header alert-header">
                <h1>🚨 Security Alert</h1>
                <p>Important security notification requires your attention</p>
            </div>
            
            <div class="content">
                <h2 style="color: #dc2626;">Hello {{{{user_name}}}},</h2>
                <p>We've detected a security-related activity on your ICEIMS 2026 account that requires your immediate attention.</p>
                
                <div class="info-box" style="background: linear-gradient(135deg, #fef2f2 0%, #fee2e2 100%); border-left-color: #dc2626;">
                    <p style="margin: 0 0 16px 0;"><strong style="color: #dc2626; font-size: 17px;">🔔 Security Event Details</strong></p>
                    <p><strong>Event Type:</strong> {{{{event_type}}}}</p>
                    <p><strong>Description:</strong> {{{{description}}}}</p>
                    <p><strong>Date & Time:</strong> {{{{time}}}}</p>
                    <p><strong>IP Address:</strong> {{{{ip_address}}}}</p>
                </div>
                
                <div class="info-box" style="background: linear-gradient(135deg, #fffbeb 0%, #fef3c7 100%); border-left-color: #f59e0b;">
                    <p style="margin: 0 0 10px 0;"><strong style="color: #b45309;">⚠️ Immediate Action Required</strong></p>
                    <p style="color: #78350f; margin: 0 0 10px 0;">If you recognize this activity, no action is needed. However, if you don't recognize it:</p>
                    <ul style="margin: 0; padding-left: 22px; color: #78350f;">
                        <li><strong>Change your password immediately</strong></li>
                        <li>Review all recent account activity</li>
                        <li>Enable two-factor authentication (OTP)</li>
                        <li>Contact our support team urgently</li>
                    </ul>
                </div>
                
                <div class="divider"></div>
                
                <p><strong>Your account security is our highest priority.</strong> We continuously monitor for suspicious activities and will notify you of any security-related events to keep your account safe.</p>
                
                <center>
                    <a href="mailto:iceims.official@gmail.com" class="button" style="background: linear-gradient(135deg, #dc2626 0%, #ef4444 100%);">Contact Security Team</a>
                </center>
            </div>
            
            <div class="footer">
                <div class="footer-logo">ICEIMS 2026</div>
                <p><strong>International Conference on Emerging & Intelligent Management Systems</strong></p>
                
                <div class="conference-details">
                    <p><strong>🔒 Security Team</strong></p>
                    <p>24/7 monitoring to protect your account and data</p>
                </div>
                
                <div class="contact-info">
                    <p>📧 <strong>Urgent Support:</strong> <a href="mailto:iceims.official@gmail.com" class="contact-link">iceims.official@gmail.com</a></p>
                    <p>🌐 <strong>Website:</strong> <a href="https://iceims2026.com" class="contact-link">www.iceims2026.com</a></p>
                    <p>🏛️ <strong>Organized By:</strong> Team Vimarsh, India</p>
                </div>
                
                <div class="disclaimer">
                    This is an automated security alert from ICEIMS 2026.<br>
                    Please respond immediately if you notice any suspicious activity.<br>
                    Contact: <a href="mailto:iceims.official@gmail.com" class="contact-link">iceims.official@gmail.com</a>
                </div>
            </div>
        </div>
    </div>
</body>
</html>
                ''',
                'body_text': '''Security Alert - ICEIMS 2026

Hello {{user_name}},

Security Event Detected:

Event Type: {{event_type}}
Description: {{description}}
Date & Time: {{time}}
IP Address: {{ip_address}}

If you don't recognize this activity, contact support immediately:
Email: iceims.official@gmail.com

Conference Information:
- Website: www.iceims2026.com
- Organized by Team Vimarsh, India

Best regards,
ICEIMS 2026 Security Team''',
            },
            {
                'name': 'OTP Verification',
                'template_type': 'otp_verification',
                'subject': 'Your ICEIMS Verification Code: {{otp_code}}',
                'body_html': f'''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>OTP Verification</title>
    {email_styles}
    <style>
        .otp-box {{
            background: linear-gradient(135deg, #fff5f3 0%, #ffe8e0 100%);
            border: 3px dashed #a0352f;
            padding: 45px;
            margin: 32px 0;
            border-radius: 12px;
            text-align: center;
            box-shadow: 0 4px 12px rgba(160, 53, 47, 0.15);
        }}
        .otp-code {{
            font-size: 56px;
            font-weight: bold;
            color: #a0352f;
            letter-spacing: 18px;
            font-family: 'Courier New', monospace;
            text-shadow: 2px 2px 4px rgba(160, 53, 47, 0.1);
            margin: 0;
        }}
        .expiry-text {{
            color: #6c757d;
            font-size: 14px;
            margin-top: 22px;
            font-weight: 600;
        }}
    </style>
</head>
<body>
    <div class="email-wrapper">
        <div class="email-container">
            <div class="logo-section">
                {logo_svg}
                <div class="conference-title">ICEIMS 2026</div>
                <p class="conference-subtitle">International Conference on<br>Emerging & Intelligent Management Systems</p>
            </div>
            
            <div class="header">
                <h1>🔐 Verification Required</h1>
                <p>One-Time Password for secure authentication</p>
            </div>
            
            <div class="content">
                <h2>Hello {{{{user_name}}}},</h2>
                <p>Please use the One-Time Password (OTP) below to complete your <strong>{{{{purpose}}}}</strong>:</p>
                
                <div class="otp-box">
                    <div class="otp-code">{{{{otp_code}}}}</div>
                    <div class="expiry-text">⏱️ Valid for <strong>{{{{expiry_minutes}}}} minutes</strong></div>
                </div>
                
                <div class="info-box" style="background: linear-gradient(135deg, #fffbeb 0%, #fef3c7 100%); border-left-color: #f59e0b;">
                    <p style="margin: 0 0 12px 0;"><strong style="color: #b45309;">⚠️ Important Security Notice</strong></p>
                    <ul style="margin: 0; padding-left: 22px; color: #78350f;">
                        <li><strong>Never share this code</strong> with anyone, including ICEIMS staff</li>
                        <li>ICEIMS team will <strong>never ask</strong> for your OTP code</li>
                        <li>This code was requested from IP: <strong>{{{{ip_address}}}}</strong></li>
                        <li>Code expires in {{{{expiry_minutes}}}} minutes and can only be used once</li>
                        <li>If you didn't request this code, please ignore this email and contact support</li>
                    </ul>
                </div>
                
                <div class="divider"></div>
                
                <p style="color: #6c757d; font-size: 14px; text-align: center;">
                    <strong>Need assistance?</strong> Our support team is available 24/7 at <a href="mailto:iceims.official@gmail.com" style="color: #a0352f; text-decoration: none; font-weight: 600;">iceims.official@gmail.com</a>
                </p>
            </div>
            
            <div class="footer">
                <div class="footer-logo">ICEIMS 2026</div>
                <p><strong>International Conference on Emerging & Intelligent Management Systems</strong></p>
                
                <div class="conference-details">
                    <p><strong>🔒 Secure Authentication</strong></p>
                    <p>Two-factor authentication ensures maximum security for your account</p>
                </div>
                
                <div class="contact-info">
                    <p>📧 <strong>Support:</strong> <a href="mailto:iceims.official@gmail.com" class="contact-link">iceims.official@gmail.com</a></p>
                    <p>🌐 <strong>Website:</strong> <a href="https://iceims2026.com" class="contact-link">www.iceims2026.com</a></p>
                    <p>🏛️ <strong>Organized By:</strong> Team Vimarsh, India</p>
                </div>
                
                <div class="disclaimer">
                    This is an automated verification email from ICEIMS 2026. Please do not reply.<br>
                    For assistance: <a href="mailto:iceims.official@gmail.com" class="contact-link">iceims.official@gmail.com</a>
                </div>
            </div>
        </div>
    </div>
</body>
</html>
                ''',
                'body_text': '''Your ICEIMS Verification Code

ICEIMS 2026 - International Conference on Emerging & Intelligent Management Systems

Hello {{user_name}},

Your One-Time Password (OTP): {{otp_code}}

Purpose: {{purpose}}
Valid for: {{expiry_minutes}} minutes
Requested from IP: {{ip_address}}

Security Notice:
- Never share this code with anyone
- ICEIMS staff will never ask for your OTP
- Code can only be used once
- Expires automatically after {{expiry_minutes}} minutes

Conference Information:
- Email: iceims.official@gmail.com
- Website: www.iceims2026.com
- Organized by Team Vimarsh, India

For assistance: iceims.official@gmail.com

Best regards,
ICEIMS 2026 Team''',
            },
            {
                'name': 'Account Created by Admin',
                'template_type': 'account_created',
                'subject': 'Your ICEIMS Admin Account - {{user_name}}',
                'body_html': f'''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Account Created</title>
    {email_styles}
    <style>
        .account-header {{
            background: linear-gradient(135deg, #8b5cf6 0%, #a78bfa 100%);
        }}
    </style>
</head>
<body>
    <div class="email-wrapper">
        <div class="email-container">
            <div class="logo-section">
                {logo_svg}
                <div class="conference-title">ICEIMS 2026</div>
                <p class="conference-subtitle">International Conference on<br>Emerging & Intelligent Management Systems</p>
            </div>
            
            <div class="header account-header">
                <h1>✨ Account Created</h1>
                <p>Your administrator account is ready to use</p>
            </div>
            
            <div class="content">
                <h2 style="color: #8b5cf6;">Hello {{{{user_name}}}},</h2>
                <p>An administrator has created an account for you on the <strong>ICEIMS 2026</strong> conference management platform. You now have access to the administrative system.</p>
                
                <div class="info-box" style="background: linear-gradient(135deg, #faf5ff 0%, #f3e8ff 100%); border-left-color: #8b5cf6;">
                    <p style="margin: 0 0 16px 0;"><strong style="font-size: 17px; color: #8b5cf6;">Your Account Credentials</strong></p>
                    <p><strong>Email Address:</strong> {{{{email}}}}</p>
                    <p><strong>Username:</strong> {{{{username}}}}</p>
                    <p><strong>Role:</strong> {{{{role}}}}</p>
                </div>
                
                <div class="info-box" style="background: linear-gradient(135deg, #fffbeb 0%, #fef3c7 100%); border-left-color: #f59e0b;">
                    <p style="margin: 0; color: #78350f;"><strong style="color: #b45309;">⚠️ Important:</strong> Please set your password upon first login or contact the administrator for access credentials.</p>
                </div>
                
                <center>
                    <a href="{{{{login_url}}}}" class="button" style="background: linear-gradient(135deg, #8b5cf6 0%, #a78bfa 100%);">Access Admin Panel</a>
                </center>
                
                <div class="divider"></div>
                
                <p><strong style="color: #8b5cf6;">🔒 Security Recommendations:</strong></p>
                <ul>
                    <li>Change your password after first login</li>
                    <li>Use a strong, unique password (minimum 12 characters)</li>
                    <li>Enable OTP two-factor authentication</li>
                    <li>Never share your account credentials</li>
                    <li>Review your account permissions and settings</li>
                </ul>
            </div>
            
            <div class="footer">
                <div class="footer-logo">ICEIMS 2026</div>
                <p><strong>International Conference on Emerging & Intelligent Management Systems</strong></p>
                
                <div class="conference-details">
                    <p><strong>📅 Conference:</strong> ICEIMS 2026</p>
                    <p><strong>📍 Location:</strong> India</p>
                    <p><strong>🏛️ Organized By:</strong> Team Vimarsh</p>
                </div>
                
                <div class="contact-info">
                    <p>📧 <strong>Support:</strong> <a href="mailto:iceims.official@gmail.com" class="contact-link">iceims.official@gmail.com</a></p>
                    <p>🌐 <strong>Website:</strong> <a href="https://iceims2026.com" class="contact-link">www.iceims2026.com</a></p>
                </div>
                
                <div class="disclaimer">
                    This is an automated notification from ICEIMS 2026.<br>
                    For assistance: <a href="mailto:iceims.official@gmail.com" class="contact-link">iceims.official@gmail.com</a>
                </div>
            </div>
        </div>
    </div>
</body>
</html>
                ''',
                'body_text': '''Your ICEIMS Account Created

ICEIMS 2026 - International Conference on Emerging & Intelligent Management Systems

Hello {{user_name}},

Your Account Details:
- Email: {{email}}
- Username: {{username}}
- Role: {{role}}

Login URL: {{login_url}}

Important: Please set your password upon first login.

Conference Information:
- Email: iceims.official@gmail.com
- Website: www.iceims2026.com
- Organized by Team Vimarsh, India

For assistance: iceims.official@gmail.com

Best regards,
ICEIMS 2026 Team''',
            },
            {
                'name': 'Role Assignment Notification',
                'template_type': 'role_assigned',
                'subject': 'Role Updated - ICEIMS 2026',
                'body_html': f'''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Role Update</title>
    {email_styles}
    <style>
        .role-header {{
            background: linear-gradient(135deg, #3b82f6 0%, #60a5fa 100%);
        }}
    </style>
</head>
<body>
    <div class="email-wrapper">
        <div class="email-container">
            <div class="logo-section">
                {logo_svg}
                <div class="conference-title">ICEIMS 2026</div>
                <p class="conference-subtitle">International Conference on<br>Emerging & Intelligent Management Systems</p>
            </div>
            
            <div class="header role-header">
                <h1>👤 Role Updated</h1>
                <p>Your account permissions have been modified</p>
            </div>
            
            <div class="content">
                <h2 style="color: #3b82f6;">Hello {{{{user_name}}}},</h2>
                <p>Your role has been updated on the ICEIMS 2026 conference platform. Your access permissions and responsibilities have been adjusted accordingly.</p>
                
                <div class="info-box" style="background: linear-gradient(135deg, #eff6ff 0%, #dbeafe 100%); border-left-color: #3b82f6;">
                    <p style="margin: 0 0 12px 0;"><strong style="font-size: 19px; color: #3b82f6;">New Role: {{{{role_name}}}}</strong></p>
                    <p style="margin: 0; color: #1e40af; line-height: 1.7;">{{{{role_description}}}}</p>
                </div>
                
                <p>Your access permissions and capabilities have been updated to match your new role. Please log in to review your updated responsibilities and explore your new administrative features.</p>
                
                <center>
                    <a href="{{{{login_url}}}}" class="button" style="background: linear-gradient(135deg, #3b82f6 0%, #60a5fa 100%);">View New Permissions</a>
                </center>
                
                <div class="divider"></div>
                
                <p style="color: #6c757d; font-size: 14px;">If you have questions about your new role, responsibilities, or need assistance with your updated permissions, please contact our support team.</p>
            </div>
            
            <div class="footer">
                <div class="footer-logo">ICEIMS 2026</div>
                <p><strong>International Conference on Emerging & Intelligent Management Systems</strong></p>
                
                <div class="conference-details">
                    <p><strong>🏛️ Organized By:</strong> Team Vimarsh, India</p>
                    <p><strong>📧 Support:</strong> Available 24/7</p>
                </div>
                
                <div class="contact-info">
                    <p>📧 <strong>Email:</strong> <a href="mailto:iceims.official@gmail.com" class="contact-link">iceims.official@gmail.com</a></p>
                    <p>🌐 <strong>Website:</strong> <a href="https://iceims2026.com" class="contact-link">www.iceims2026.com</a></p>
                </div>
                
                <div class="disclaimer">
                    This is an automated notification from ICEIMS 2026.<br>
                    For questions: <a href="mailto:iceims.official@gmail.com" class="contact-link">iceims.official@gmail.com</a>
                </div>
            </div>
        </div>
    </div>
</body>
</html>
                ''',
                'body_text': '''Role Updated - ICEIMS 2026

Hello {{user_name}},

Your role has been updated:

New Role: {{role_name}}
Description: {{role_description}}

Your access permissions have been updated accordingly.

Conference Information:
- Email: iceims.official@gmail.com
- Website: www.iceims2026.com
- Organized by Team Vimarsh, India

For assistance: iceims.official@gmail.com

Best regards,
ICEIMS 2026 Team''',
            },
        ]
        
        created_count = 0
        updated_count = 0
        
        for template_data in templates:
            template, created = EmailTemplate.objects.update_or_create(
                name=template_data['name'],
                defaults={
                    **template_data,
                    'created_by': superuser,
                }
            )
            
            if created:
                created_count += 1
                self.stdout.write(self.style.SUCCESS(f'✓ Created: {template.name}'))
            else:
                updated_count += 1
                self.stdout.write(self.style.WARNING(f'⟳ Updated: {template.name}'))
        
        self.stdout.write(self.style.SUCCESS(f'\n📧 Summary: Created {created_count}, Updated {updated_count} templates'))
        self.stdout.write(self.style.SUCCESS('✅ All professional email templates are ready with ICEIMS website branding!'))
        self.stdout.write(self.style.SUCCESS('🎨 Matching website theme colors: #a0352f & #e56d2d'))
        self.stdout.write(self.style.SUCCESS('📍 Contact: iceims.official@gmail.com'))
