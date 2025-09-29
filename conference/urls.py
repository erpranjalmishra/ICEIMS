from django.urls import path
from . import views

app_name = 'conference'

urlpatterns = [
    # Main Conference Pages
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('tracks/', views.tracks, name='tracks'),
    path('committee/members/', views.committee, name='committee'),
    path('committee/speakers/', views.keynotes, name='speakers'),
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
    
    # Public Blog URLs (No authentication required for viewing)
    path('blog/', views.blog_public_list, name='blog_public_list'),
    path('blog/<slug:slug>/', views.blog_public_detail, name='blog_public_detail'),
    path('blog/category/<slug:slug>/', views.blog_category_view, name='blog_category_view'),
    
    # Authentication URLs
    path('login/', views.user_login, name='login'),
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
]