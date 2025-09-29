from django.urls import path
from . import views

app_name = 'conference'

urlpatterns = [
    # Main Conference Pages
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('tracks/', views.tracks, name='tracks'),
    path('committee/members/', views.committee, name='committee'),
    path('committee/speakers/', views.keynotes, name='keynotes'),
    path('speakers/', views.keynotes, name='speakers'),
    path('attractions/', views.attractions, name='attractions'),
    path('contact/', views.contact, name='contact'),
    path('guidelines/', views.guidelines, name='guidelines'),
    path('registration/', views.registration, name='registration'),
    path('workshops/', views.workshops, name='workshops'),
    path('panels/', views.panels, name='panels'),
    path('networking/', views.networking, name='networking'),
    path('previous/', views.previous, name='previous'),
    path('schedule/', views.schedule, name='schedule'),
    path('awards/', views.awards, name='awards'),
    path('sponsors/', views.sponsors, name='sponsors'),
    
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
    
    # Maintenance Mode Management URLs (Admin/Staff only)
    path('admin-panel/maintenance/', views.maintenance_list, name='maintenance_list'),
    path('admin-panel/maintenance/create/', views.maintenance_create, name='maintenance_create'),
    path('admin-panel/maintenance/<int:pk>/toggle/', views.maintenance_toggle, name='maintenance_toggle'),
    
    # Notice Management URLs (Admin/Staff only)
    path('admin-panel/notices/', views.notice_list, name='notice_list'),
    path('admin-panel/notices/create/', views.notice_create, name='notice_create'),
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
    path('admin-panel/roles/', views.role_management, name='role_management'),
    path('admin-panel/roles/create/', views.role_create, name='role_create'),
]