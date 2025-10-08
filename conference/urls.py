from django.urls import path
from . import views
from .debug_views import media_debug

app_name = 'conference'

urlpatterns = [
    # Main Conference Pages
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('university/', views.university, name='university'),
    path('sitemap/', views.sitemap, name='sitemap'),
    path('tracks/', views.tracks, name='tracks'),
    path('committee/members/', views.committee, name='committee'),
    path('committee/members/<slug:slug>/', views.committee_bio, name='committee_bio'),
    path('committee/speakers/', views.keynotes, name='keynotes'),
    path('speakers/', views.keynotes, name='speakers'),
    path('speakers/<slug:slug>/', views.speaker_bio, name='speaker_bio'),
    path('attractions/', views.attractions, name='attractions'),
    path('attractions/<slug:slug>/', views.attraction_detail, name='attraction_detail'),
    path('contact/', views.contact, name='contact'),
    path('guidelines/', views.guidelines, name='guidelines'),
    path('registration/', views.registration, name='registration'),
    path('registration/success/<str:reg_id>/', views.registration_success, name='registration_success'),
    path('workshops/', views.workshops, name='workshops'),
    path('panels/', views.panels, name='panels'),
    path('networking/', views.networking, name='networking'),
    path('previous/', views.previous, name='previous'),
    path('schedule/', views.schedule, name='schedule'),
    path('awards/', views.awards, name='awards'),
    path('sponsors/', views.sponsors, name='sponsors'),
    path('faq/', views.faq_page, name='faq'),
    path('downloads/', views.downloads, name='downloads'),
    path('downloads/<int:resource_id>/download/', views.download_file, name='download_file'),
    
    # API endpoints
    path('api/visitor-count/', views.get_visitor_count, name='get_visitor_count'),
    
    # Debug URLs (Staff only)
    path('admin-panel/debug/media/', media_debug, name='media_debug'),
    
    # FAQ AJAX endpoints
    path('faq/ask-ai/', views.faq_ask_ai, name='faq_ask_ai'),
    path('faq/<int:faq_id>/helpful/', views.faq_mark_helpful, name='faq_mark_helpful'),
    path('faq/<int:faq_id>/not-helpful/', views.faq_mark_not_helpful, name='faq_mark_not_helpful'),
    path('faq/conversation/<int:conversation_id>/feedback/', views.faq_conversation_feedback, name='faq_conversation_feedback'),
    
    # Hidden test page - not linked in navigation
    path('secret-animations-test/', views.animations_test, name='animations_test'),
    
    # Test error pages in development (remove in production)
    path('test-404/', views.test_404, name='test_404'),
    path('test-500/', views.test_500, name='test_500'),
    
    # Public Blog URLs (No authentication required for viewing)
    path('blog/', views.blog_public_list, name='blog_public_list'),
    path('blog/<slug:slug>/', views.blog_public_detail, name='blog_public_detail'),
    path('blog/category/<slug:slug>/', views.blog_category_view, name='blog_category_view'),
    
    # Authentication URLs
    path('login/', views.user_login, name='login'),
    path('admin-login/', views.admin_login, name='admin_login'),
    path('register/', views.user_register, name='register'),
    path('logout/', views.user_logout, name='logout'),
    path('newsletter/signup/', views.newsletter_signup, name='newsletter_signup'),
    
    # Blog Management URLs (Admin/Staff only)
    path('blog-admin/', views.blog_list, name='blog_list'),
    path('blog-admin/create/', views.blog_create, name='blog_create'),
    path('blog-admin/<slug:slug>/edit/', views.blog_edit, name='blog_edit'),
    path('blog-admin/<slug:slug>/delete/', views.blog_delete, name='blog_delete'),
    path('blog-admin/bulk-action/', views.blog_bulk_action, name='blog_bulk_action'),
    path('blog-admin/analytics/', views.blog_analytics, name='blog_analytics'),
    
    # Category Management URLs (Admin/Staff only)
    path('blog-admin/categories/', views.category_list, name='category_list'),
    path('blog-admin/categories/create/', views.category_create, name='category_create'),
    path('blog-admin/categories/<int:pk>/delete/', views.category_delete, name='category_delete'),
    
    # Comment Management URLs (Admin/Staff only)
    path('blog-admin/comments/', views.comment_list, name='comment_list'),
    path('blog-admin/comments/<int:comment_id>/approve/', views.comment_approve, name='comment_approve'),
    path('blog-admin/comments/<int:comment_id>/reject/', views.comment_reject, name='comment_reject'),
    path('blog-admin/comments/<int:comment_id>/delete/', views.comment_delete, name='comment_delete'),
    path('blog-admin/comments/bulk-action/', views.comment_bulk_action, name='comment_bulk_action'),
    
    # Admin Dashboard
    path('admin-panel/', views.admin_dashboard, name='admin_dashboard'),
    path('admin-panel/sitemap/', views.admin_sitemap, name='admin_sitemap'),
    
    # Maintenance Mode Management URLs (Admin/Staff only)
    path('admin-panel/maintenance/', views.maintenance_list, name='maintenance_list'),
    path('admin-panel/maintenance/create/', views.maintenance_create, name='maintenance_create'),
    path('admin-panel/maintenance/<int:pk>/toggle/', views.maintenance_toggle, name='maintenance_toggle'),
    
    # Notice Management URLs (Admin/Staff only)
    path('admin-panel/notices/', views.notice_list, name='notice_list'),
    path('admin-panel/notices/create/', views.notice_create, name='notice_create'),
    path('admin-panel/notices/<int:pk>/edit/', views.notice_edit, name='notice_edit'),
    path('admin-panel/notices/<int:pk>/toggle/', views.notice_toggle, name='notice_toggle'),
    path('admin-panel/notices/<int:pk>/delete/', views.notice_delete, name='notice_delete'),
    
    # Timeline Management URLs (Admin/Staff only)
    path('admin-panel/timeline/', views.timeline_list, name='timeline_list'),
    path('admin-panel/timeline/create/', views.timeline_create, name='timeline_create'),
    path('admin-panel/timeline/<int:pk>/edit/', views.timeline_edit, name='timeline_edit'),
    path('admin-panel/timeline/<int:pk>/delete/', views.timeline_delete, name='timeline_delete'),
    
    # Status Update Management URLs (Admin/Staff only)
    path('admin-panel/status-updates/', views.status_update_list, name='status_update_list'),
    path('admin-panel/status-updates/create/', views.status_update_create, name='status_update_create'),
    path('admin-panel/status-updates/<int:pk>/edit/', views.status_update_edit, name='status_update_edit'),
    path('admin-panel/status-updates/<int:pk>/delete/', views.status_update_delete, name='status_update_delete'),
    path('admin-panel/status-updates/<int:pk>/toggle/', views.status_update_toggle, name='status_update_toggle'),
    
    # Schedule Management URLs (Admin/Staff only)
    path('admin-panel/schedule/', views.schedule_list, name='schedule_list'),
    path('admin-panel/schedule/create/', views.schedule_create, name='schedule_create'),
    path('admin-panel/schedule/<int:pk>/edit/', views.schedule_edit, name='schedule_edit'),
    path('admin-panel/schedule/<int:pk>/delete/', views.schedule_delete, name='schedule_delete'),
    path('admin-panel/schedule/<int:pk>/toggle/', views.schedule_toggle, name='schedule_toggle'),
    
    # Speaker Management URLs (Admin/Staff only)
    path('admin-panel/speakers/', views.speaker_list, name='speaker_list'),
    path('admin-panel/speakers/create/', views.speaker_create, name='speaker_create'),
    path('admin-panel/speakers/<int:pk>/edit/', views.speaker_edit, name='speaker_edit'),
    path('admin-panel/speakers/<int:pk>/delete/', views.speaker_delete, name='speaker_delete'),
    path('admin-panel/speakers/<int:pk>/toggle/', views.speaker_toggle, name='speaker_toggle'),
    
    # Committee Management URLs (Admin/Staff only)
    path('admin-panel/committee/', views.committee_list, name='committee_list'),
    path('admin-panel/committee/create/', views.committee_create, name='committee_create'),
    path('admin-panel/committee/<int:pk>/edit/', views.committee_edit, name='committee_edit'),
    path('admin-panel/committee/<int:pk>/delete/', views.committee_delete, name='committee_delete'),
    path('admin-panel/committee/reorder/', views.committee_reorder, name='committee_reorder'),
    
    # Track Management URLs (Admin/Staff only)
    path('admin-panel/tracks/', views.track_list, name='track_list'),
    path('admin-panel/tracks/create/', views.track_create, name='track_create'),
    path('admin-panel/tracks/<int:pk>/edit/', views.track_edit, name='track_edit'),
    path('admin-panel/tracks/<int:pk>/delete/', views.track_delete, name='track_delete'),
    path('admin-panel/tracks/<int:pk>/toggle/', views.track_toggle, name='track_toggle'),
    path('admin-panel/tracks/bulk-action/', views.track_bulk_action, name='track_bulk_action'),
    
    # Tourist Attraction Management URLs (Admin/Staff only)
    path('admin-panel/attractions/', views.attraction_list, name='attraction_list'),
    path('admin-panel/attractions/create/', views.attraction_create, name='attraction_create'),
    path('admin-panel/attractions/<int:pk>/edit/', views.attraction_edit, name='attraction_edit'),
    path('admin-panel/attractions/<int:pk>/delete/', views.attraction_delete, name='attraction_delete'),
    path('admin-panel/attractions/<int:pk>/toggle/', views.attraction_toggle, name='attraction_toggle'),
    path('admin-panel/attractions/bulk-action/', views.attraction_bulk_action, name='attraction_bulk_action'),
    
    # Sponsor Management URLs (Admin/Staff only)
    path('admin-panel/sponsors/', views.sponsor_list, name='sponsor_list'),
    path('admin-panel/sponsors/create/', views.sponsor_create, name='sponsor_create'),
    path('admin-panel/sponsors/<int:pk>/edit/', views.sponsor_edit, name='sponsor_edit'),
    path('admin-panel/sponsors/<int:pk>/delete/', views.sponsor_delete, name='sponsor_delete'),
    path('admin-panel/sponsors/bulk-action/', views.sponsor_bulk_action, name='sponsor_bulk_action'),
    
    # Export URLs (Admin/Staff only)
    path('admin-panel/export/speakers/', views.export_speakers, name='export_speakers'),
    path('admin-panel/export/committee/', views.export_committee, name='export_committee'),
    path('admin-panel/export/schedule/', views.export_schedule, name='export_schedule'),
    path('admin-panel/export/logs/', views.export_logs, name='export_logs'),
    
    # User Management URLs (Superuser/User Admin only)
    path('admin-panel/users/', views.user_management, name='user_management'),
    path('admin-panel/users/create/', views.user_create, name='user_create'),
    path('admin-panel/users/<int:user_id>/edit/', views.user_edit, name='user_edit'),
    path('admin-panel/users/<int:user_id>/delete/', views.user_delete, name='user_delete'),
    path('admin-panel/users/fix-staff-status/', views.fix_user_staff_status, name='fix_user_staff_status'),
    path('admin-panel/roles/', views.role_management, name='role_management'),
    path('admin-panel/roles/create/', views.role_create, name='role_create'),
    
    # Email Management URLs (Superuser only)
    path('admin-panel/emails/templates/', views.email_template_list, name='email_template_list'),
    path('admin-panel/emails/templates/create/', views.email_template_create, name='email_template_create'),
    path('admin-panel/emails/templates/<int:pk>/edit/', views.email_template_edit, name='email_template_edit'),
    path('admin-panel/emails/templates/<int:pk>/delete/', views.email_template_delete, name='email_template_delete'),
    path('admin-panel/emails/templates/<int:pk>/preview/', views.email_template_preview, name='email_template_preview'),
    path('admin-panel/emails/logs/', views.email_log_list, name='email_log_list'),
    path('admin-panel/emails/campaigns/', views.email_campaign_list, name='email_campaign_list'),
    path('admin-panel/emails/campaigns/create/', views.email_campaign_create, name='email_campaign_create'),
    path('admin-panel/emails/campaigns/<int:pk>/send/', views.email_campaign_send, name='email_campaign_send'),
    path('admin-panel/emails/security/', views.security_event_list, name='security_event_list'),
    
    # Email Sending URLs
    path('admin-panel/emails/send/', views.send_email, name='send_email'),
    path('admin-panel/emails/scheduled/', views.scheduled_emails, name='scheduled_emails'),
    path('admin-panel/emails/scheduled/<int:pk>/send-now/', views.send_scheduled_email_now, name='send_scheduled_email_now'),
    path('admin-panel/emails/scheduled/<int:pk>/cancel/', views.cancel_scheduled_email, name='cancel_scheduled_email'),
    path('admin-panel/emails/settings/', views.email_settings, name='email_settings'),
]