from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, JsonResponse, HttpResponseForbidden
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q, Count
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_protect, ensure_csrf_cookie
from django.utils.text import slugify
from django.utils import timezone
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import views as auth_views
from .models import (
    CommitteeMember, ConferenceTrack, TouristAttraction, 
    ImportantDate, Slider, ConferenceSettings, Sponsor,
    BlogPost, Category, Tag, Comment, Newsletter,
    MaintenanceMode, Notice
)

def home(request):
    """Home page view with all conference information"""
    
    # Get active notices for home page
    current_time = timezone.now()
    notices = Notice.objects.filter(
        is_active=True,
        start_date__lte=current_time
    ).filter(
        Q(end_date__isnull=True) | Q(end_date__gte=current_time)
    ).filter(
        Q(show_on_pages='') | Q(show_on_pages__icontains='home') | Q(show_on_pages__icontains='all')
    ).order_by('-is_urgent', '-created_at')
    
    # Get timeline items for home page
    from .models import Timeline
    timeline_items = Timeline.objects.filter(
        is_public=True
    ).order_by('date')[:6]  # Show first 6 items
    
    # Get all data for the homepage
    context = {
        # Notices
        'notices': notices,
        
        # Timeline items
        'timeline_items': timeline_items,
        
        # Slider images
        'slider_images': Slider.objects.filter(is_active=True),
        
        # Committee members
        'committee_members': CommitteeMember.objects.all(),
        
        # Conference tracks
        'regular_tracks': ConferenceTrack.objects.filter(track_type='regular'),
        'special_tracks': ConferenceTrack.objects.filter(track_type='special'),
        
        # Tourist attractions
        'tourist_attractions': TouristAttraction.objects.all(),
        
        # Important dates
        'important_dates': ImportantDate.objects.all(),
        
        # Sponsors
        'sponsors': Sponsor.objects.all(),
        
        # Conference settings
        'conference_settings': ConferenceSettings.objects.first(),
    }
    
    return render(request, 'home.html', context)

def about(request):
    """About page view"""
    conference_settings = ConferenceSettings.objects.first()
    return render(request, 'about.html', {'conference_settings': conference_settings})

def tracks(request):
    """Conference tracks page"""
    context = {
        'regular_tracks': ConferenceTrack.objects.filter(track_type='regular'),
        'special_tracks': ConferenceTrack.objects.filter(track_type='special'),
    }
    return render(request, 'tracks.html', context)

def committee(request):
    """Committee members page"""
    committee_members = CommitteeMember.objects.filter(is_active=True).order_by('hierarchy_level', 'order', 'name')
    return render(request, 'committee.html', {'committee_members': committee_members})

def attractions(request):
    """Tourist attractions page"""
    attractions = TouristAttraction.objects.all()
    return render(request, 'attractions.html', {'attractions': attractions})

def contact(request):
    """Contact page view"""
    return render(request, 'contact.html')

def guidelines(request):
    """Guidelines page view"""
    return render(request, 'guidelines.html')

def keynotes(request):
    """Keynote speakers page view with dynamic data"""
    from .models import Speaker
    
    # Get published speakers
    speakers = Speaker.objects.filter(is_published=True).order_by('display_order', 'name')
    keynote_speakers = speakers.filter(speaker_type='keynote')
    invited_speakers = speakers.filter(speaker_type='invited')
    featured_speakers = speakers.filter(is_featured=True)
    
    context = {
        'speakers': speakers,
        'keynote_speakers': keynote_speakers,
        'invited_speakers': invited_speakers,
        'featured_speakers': featured_speakers,
    }
    return render(request, 'keynotes.html', context)

def registration(request):
    """Registration rates page view"""
    return render(request, 'registration.html')

def workshops(request):
    """Workshops page view"""
    return render(request, 'workshops.html')

def panels(request):
    """Panel discussions page view"""
    return render(request, 'panels.html')

def networking(request):
    """Networking events page view"""
    return render(request, 'networking.html')

def previous(request):
    """Previous conferences page view"""
    return render(request, 'previous.html')

def schedule(request):
    """Schedule page view with dynamic schedule data"""
    from .models import Schedule
    
    # Get published schedule items
    schedules = Schedule.objects.filter(is_published=True).order_by('date', 'start_time')
    
    # Group schedules by day
    schedule_by_day = {}
    for schedule in schedules:
        day = schedule.get_day_display()
        if day not in schedule_by_day:
            schedule_by_day[day] = []
        schedule_by_day[day].append(schedule)
    
    # Calculate statistics
    total_days = len(schedule_by_day)
    keynote_sessions = schedules.filter(schedule_type='keynote').count()
    technical_sessions = schedules.filter(schedule_type='presentation').count()
    workshop_sessions = schedules.filter(schedule_type='workshop').count()
    
    context = {
        'schedules': schedules,
        'schedule_by_day': schedule_by_day,
        'total_days': total_days,
        'keynote_sessions': keynote_sessions,
        'technical_sessions': technical_sessions,
        'workshop_sessions': workshop_sessions,
    }
    return render(request, 'schedule.html', context)

def awards(request):
    """Awards page view"""
    return render(request, 'awards.html')

def sponsors(request):
    """Sponsors page view"""
    sponsors = Sponsor.objects.all()
    context = {
        'sponsors': sponsors,
        # For now, display all sponsors without tiers since the model doesn't have a tier field
        'all_sponsors': sponsors,
    }
    return render(request, 'sponsors.html', context)

def animations_test(request):
    """Hidden animations test page - not linked in navigation"""
    return render(request, 'animations-test.html')

# Blog Helper Functions

def is_admin_or_staff(user):
    return user.is_authenticated and (user.is_staff or user.is_superuser)

# Public Blog Views (No authentication required for viewing)
@ensure_csrf_cookie
def blog_public_list(request):
    """Public blog list - no authentication required"""
    posts = BlogPost.objects.filter(status='published').order_by('-published_at')
    
    # Search functionality
    search = request.GET.get('search')
    if search:
        posts = posts.filter(
            Q(title__icontains=search) | 
            Q(content__icontains=search) |
            Q(excerpt__icontains=search)
        )
    
    # Filter by category
    category_slug = request.GET.get('category')
    if category_slug:
        posts = posts.filter(category__slug=category_slug)
    
    # Pagination
    paginator = Paginator(posts, 6)
    page_number = request.GET.get('page')
    posts = paginator.get_page(page_number)
    
    categories = Category.objects.all()
    featured_posts = BlogPost.objects.filter(status='published', featured=True)[:3]
    
    context = {
        'posts': posts,
        'categories': categories,
        'featured_posts': featured_posts,
        'search': search,
        'category_slug': category_slug,
    }
    
    return render(request, 'blog/public/blog_list.html', context)

@ensure_csrf_cookie
def blog_public_detail(request, slug):
    """Public blog detail view - no authentication required"""
    post = get_object_or_404(BlogPost, slug=slug, status='published')
    
    # Increment view count
    post.increment_views()
    
    # Get approved comments
    comments = post.comments.filter(status='approved').order_by('-created_at')
    
    # Handle comment submission (requires login)
    if request.method == 'POST' and request.user.is_authenticated:
        name = request.POST.get('name')
        email = request.POST.get('email')
        website = request.POST.get('website', '')
        content = request.POST.get('content')
        
        if name and email and content:
            # Get user's IP address
            x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
            if x_forwarded_for:
                ip = x_forwarded_for.split(',')[0]
            else:
                ip = request.META.get('REMOTE_ADDR')
            
            Comment.objects.create(
                post=post,
                name=name,
                email=email,
                website=website,
                content=content,
                ip_address=ip,
                user_agent=request.META.get('HTTP_USER_AGENT', ''),
                status='pending'
            )
            
            messages.success(request, 'Your comment has been submitted and is awaiting approval.')
            return redirect('conference:blog_public_detail', slug=slug)
    
    # Related posts
    related_posts = BlogPost.objects.filter(
        status='published',
        category=post.category
    ).exclude(id=post.id)[:3]
    
    # Popular posts
    popular_posts = BlogPost.objects.filter(status='published').order_by('-views')[:5]
    
    context = {
        'post': post,
        'comments': comments,
        'related_posts': related_posts,
        'popular_posts': popular_posts,
    }
    
    return render(request, 'blog/public/blog_detail.html', context)

def blog_category_view(request, slug):
    """Public category view"""
    category = get_object_or_404(Category, slug=slug)
    posts = BlogPost.objects.filter(
        status='published',
        category=category
    ).order_by('-published_at')
    
    # Pagination
    paginator = Paginator(posts, 6)
    page_number = request.GET.get('page')
    posts = paginator.get_page(page_number)
    
    context = {
        'category': category,
        'posts': posts,
    }
    
    return render(request, 'blog/public/blog_category.html', context)

# Authentication Views
@ensure_csrf_cookie
def user_login(request):
    """Custom login view"""
    if request.user.is_authenticated:
        if request.user.is_staff or request.user.is_superuser:
            return redirect('conference:admin_dashboard')
        return redirect('conference:home')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            next_url = request.GET.get('next')
            
            # Redirect admin users to dashboard
            if user.is_staff or user.is_superuser:
                if not next_url or next_url == '/':
                    next_url = 'conference:admin_dashboard'
            else:
                if not next_url:
                    next_url = 'conference:home'
            
            messages.success(request, f'Welcome back, {user.get_full_name() or user.username}!')
            return redirect(next_url)
        else:
            messages.error(request, 'Invalid username or password.')
    
    return render(request, 'auth/login.html')

def admin_login(request):
    """Dedicated admin login view"""
    if request.user.is_authenticated:
        if request.user.is_staff or request.user.is_superuser:
            return redirect('conference:admin_dashboard')
        else:
            messages.warning(request, 'You need admin privileges to access this area.')
            return redirect('conference:home')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        remember_me = request.POST.get('remember_me')
        
        # Try to authenticate by username or email
        user = authenticate(request, username=username, password=password)
        if not user:
            # Try email login
            try:
                from django.contrib.auth.models import User
                user_obj = User.objects.get(email=username)
                user = authenticate(request, username=user_obj.username, password=password)
            except User.DoesNotExist:
                pass
        
        if user is not None:
            # Check if user has admin privileges
            if user.is_staff or user.is_superuser:
                login(request, user)
                
                # Set session expiry based on remember me
                if remember_me:
                    request.session.set_expiry(30 * 24 * 60 * 60)  # 30 days
                else:
                    request.session.set_expiry(4 * 60 * 60)  # 4 hours
                
                # Create or update user session tracking
                from .models import UserSession
                import uuid
                
                # Clean up old sessions for this user
                UserSession.objects.filter(user=user, is_active=True).update(is_active=False)
                
                # Create new session record
                x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
                if x_forwarded_for:
                    ip = x_forwarded_for.split(',')[0]
                else:
                    ip = request.META.get('REMOTE_ADDR', '127.0.0.1')
                
                UserSession.objects.create(
                    user=user,
                    session_key=request.session.session_key or str(uuid.uuid4()),
                    ip_address=ip,
                    user_agent=request.META.get('HTTP_USER_AGENT', ''),
                    is_active=True
                )
                
                next_url = request.GET.get('next') or 'conference:admin_dashboard'
                messages.success(request, f'Welcome back, {user.get_full_name() or user.username}!')
                return redirect(next_url)
            else:
                messages.error(request, 'You do not have permission to access the admin panel.')
        else:
            messages.error(request, 'Invalid credentials. Please check your username/email and password.')
    
    return render(request, 'admin/admin_login.html')

@ensure_csrf_cookie
def user_register(request):
    """User registration view"""
    if request.user.is_authenticated:
        return redirect('conference:home')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        
        # Basic validation
        if not all([username, email, password1, password2]):
            messages.error(request, 'Please fill in all required fields.')
        elif password1 != password2:
            messages.error(request, 'Passwords do not match.')
        elif len(password1) < 8:
            messages.error(request, 'Password must be at least 8 characters long.')
        elif User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists.')
        elif User.objects.filter(email=email).exists():
            messages.error(request, 'Email already registered.')
        else:
            try:
                user = User.objects.create_user(
                    username=username,
                    email=email,
                    password=password1,
                    first_name=first_name,
                    last_name=last_name
                )
                messages.success(request, 'Registration successful! Please log in.')
                return redirect('conference:login')
            except Exception as e:
                messages.error(request, 'Registration failed. Please try again.')
    
    return render(request, 'auth/register.html')

def user_logout(request):
    """User logout view"""
    logout(request)
    messages.success(request, 'You have been successfully logged out.')
    return redirect('conference:home')

@require_POST
def newsletter_signup(request):
    """Newsletter signup view"""
    email = request.POST.get('email')
    
    if not email:
        messages.error(request, 'Please provide a valid email address.')
        return redirect(request.META.get('HTTP_REFERER', 'conference:home'))
    
    # Check if email already exists
    if Newsletter.objects.filter(email=email).exists():
        messages.info(request, 'You are already subscribed to our newsletter!')
    else:
        Newsletter.objects.create(email=email)
        messages.success(request, 'Thank you for subscribing to our newsletter!')
    
    return redirect(request.META.get('HTTP_REFERER', 'conference:home'))

# Blog List View
@ensure_csrf_cookie
@login_required
@user_passes_test(is_admin_or_staff)
def blog_list(request):
    posts = BlogPost.objects.all().order_by('-created_at')
    
    # Search functionality
    search = request.GET.get('search')
    if search:
        posts = posts.filter(
            Q(title__icontains=search) | 
            Q(content__icontains=search) |
            Q(excerpt__icontains=search)
        )
    
    # Filter by status
    status = request.GET.get('status')
    if status:
        posts = posts.filter(status=status)
    
    # Filter by category
    category_id = request.GET.get('category')
    if category_id:
        posts = posts.filter(category_id=category_id)
    
    # Pagination
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    posts = paginator.get_page(page_number)
    
    categories = Category.objects.all()
    pending_comments = Comment.objects.filter(status='pending').count()
    
    context = {
        'posts': posts,
        'categories': categories,
        'search': search,
        'status': status,
        'category_id': int(category_id) if category_id else None,
        'pending_comments': pending_comments,
    }
    
    return render(request, 'blog/blog_list.html', context)

# Create Blog Post
@ensure_csrf_cookie
@login_required
@user_passes_test(is_admin_or_staff)
def blog_create(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        slug = request.POST.get('slug') or slugify(title)
        category_id = request.POST.get('category')
        content = request.POST.get('content')
        excerpt = request.POST.get('excerpt')
        status = request.POST.get('status', 'draft')
        featured = request.POST.get('featured') == 'on'
        meta_description = request.POST.get('meta_description')
        meta_keywords = request.POST.get('meta_keywords')
        
        # Handle tags
        tags_str = request.POST.get('tags', '')
        tag_names = [tag.strip() for tag in tags_str.split(',') if tag.strip()]
        
        try:
            category = Category.objects.get(id=category_id)
            
            # Check if slug is unique
            if BlogPost.objects.filter(slug=slug).exists():
                slug = f"{slug}-{timezone.now().strftime('%Y%m%d%H%M%S')}"
            
            post = BlogPost.objects.create(
                title=title,
                slug=slug,
                author=request.user,
                category=category,
                content=content,
                excerpt=excerpt,
                status=status,
                featured=featured,
                meta_description=meta_description,
                meta_keywords=meta_keywords,
            )
            
            # Handle featured image
            if 'featured_image' in request.FILES:
                post.featured_image = request.FILES['featured_image']
                post.save()
            
            # Handle tags
            for tag_name in tag_names:
                tag, created = Tag.objects.get_or_create(
                    name=tag_name,
                    defaults={'slug': slugify(tag_name)}
                )
                post.tags.add(tag)
            
            messages.success(request, f'Blog post "{title}" created successfully!')
            return redirect('conference:blog_list')
            
        except Category.DoesNotExist:
            messages.error(request, 'Please select a valid category.')
        except Exception as e:
            messages.error(request, f'Error creating blog post: {str(e)}')
    
    categories = Category.objects.all()
    tags = Tag.objects.all()
    
    context = {
        'categories': categories,
        'tags': tags,
    }
    
    return render(request, 'blog/blog_create.html', context)

# Edit Blog Post
@ensure_csrf_cookie
@login_required
@user_passes_test(is_admin_or_staff)
def blog_edit(request, slug):
    post = get_object_or_404(BlogPost, slug=slug)
    
    if request.method == 'POST':
        post.title = request.POST.get('title')
        post.slug = request.POST.get('slug', slugify(post.title))
        post.category_id = request.POST.get('category')
        post.content = request.POST.get('content')
        post.excerpt = request.POST.get('excerpt')
        post.status = request.POST.get('status', 'draft')
        post.featured = request.POST.get('featured') == 'on'
        post.meta_description = request.POST.get('meta_description')
        post.meta_keywords = request.POST.get('meta_keywords')
        
        # Handle featured image
        if 'featured_image' in request.FILES:
            post.featured_image = request.FILES['featured_image']
        
        # Handle tags
        tags_str = request.POST.get('tags', '')
        tag_names = [tag.strip() for tag in tags_str.split(',') if tag.strip()]
        
        post.tags.clear()
        for tag_name in tag_names:
            tag, created = Tag.objects.get_or_create(
                name=tag_name,
                defaults={'slug': slugify(tag_name)}
            )
            post.tags.add(tag)
        
        post.save()
        messages.success(request, f'Blog post "{post.title}" updated successfully!')
        return redirect('conference:blog_list')
    
    categories = Category.objects.all()
    tags = Tag.objects.all()
    post_tags = ', '.join([tag.name for tag in post.tags.all()])
    
    context = {
        'post': post,
        'categories': categories,
        'tags': tags,
        'post_tags': post_tags,
    }
    
    return render(request, 'blog/blog_edit.html', context)

# Delete Blog Post
@login_required
@user_passes_test(is_admin_or_staff)
@require_POST
def blog_delete(request, slug):
    post = get_object_or_404(BlogPost, slug=slug)
    title = post.title
    
    # Delete featured image file if exists
    if post.featured_image:
        try:
            post.featured_image.delete()
        except:
            pass
    
    post.delete()
    messages.success(request, f'Blog post "{title}" deleted successfully!')
    return redirect('conference:blog_list')

# Category Management
@login_required
@user_passes_test(is_admin_or_staff)
def category_list(request):
    categories = Category.objects.annotate(post_count=Count('posts')).order_by('name')
    
    context = {
        'categories': categories,
    }
    
    return render(request, 'blog/category_list.html', context)

@login_required
@user_passes_test(is_admin_or_staff)
def category_create(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        slug = request.POST.get('slug') or slugify(name)
        description = request.POST.get('description')
        
        try:
            Category.objects.create(
                name=name,
                slug=slug,
                description=description
            )
            messages.success(request, f'Category "{name}" created successfully!')
            return redirect('conference:category_list')
        except Exception as e:
            messages.error(request, f'Error creating category: {str(e)}')
    
    return render(request, 'blog/category_create.html')

@login_required
@user_passes_test(is_admin_or_staff)
@require_POST
def category_delete(request, pk):
    category = get_object_or_404(Category, pk=pk)
    
    if category.posts.exists():
        messages.error(request, f'Cannot delete category "{category.name}" because it has associated blog posts.')
    else:
        name = category.name
        category.delete()
        messages.success(request, f'Category "{name}" deleted successfully!')
    
    return redirect('conference:category_list')

# Bulk Actions
@login_required
@user_passes_test(is_admin_or_staff)
@require_POST
def blog_bulk_action(request):
    action = request.POST.get('action')
    selected_ids = request.POST.getlist('selected_posts')
    
    if not selected_ids:
        messages.error(request, 'No posts selected.')
        return redirect('conference:blog_list')
    
    posts = BlogPost.objects.filter(id__in=selected_ids)
    
    if action == 'delete':
        count = posts.count()
        for post in posts:
            if post.featured_image:
                try:
                    post.featured_image.delete()
                except:
                    pass
        posts.delete()
        messages.success(request, f'Successfully deleted {count} blog posts.')
    
    elif action == 'publish':
        count = posts.update(status='published', published_at=timezone.now())
        messages.success(request, f'Successfully published {count} blog posts.')
    
    elif action == 'draft':
        count = posts.update(status='draft')
        messages.success(request, f'Successfully moved {count} blog posts to draft.')
    
    elif action == 'archive':
        count = posts.update(status='archived')
        messages.success(request, f'Successfully archived {count} blog posts.')
    
    return redirect('conference:blog_list')

# Analytics Dashboard
@login_required
@user_passes_test(is_admin_or_staff)
def blog_analytics(request):
    total_posts = BlogPost.objects.count()
    published_posts = BlogPost.objects.filter(status='published').count()
    draft_posts = BlogPost.objects.filter(status='draft').count()
    total_views = sum(BlogPost.objects.values_list('views', flat=True))
    
    # Recent posts
    recent_posts = BlogPost.objects.order_by('-created_at')[:5]
    
    # Popular posts
    popular_posts = BlogPost.objects.filter(status='published').order_by('-views')[:5]
    
    # Comments stats
    total_comments = Comment.objects.count()
    pending_comments = Comment.objects.filter(status='pending').count()
    
    # Calculate percentages
    published_percentage = round((published_posts * 100) / total_posts, 1) if total_posts > 0 else 0
    draft_percentage = round((draft_posts * 100) / total_posts, 1) if total_posts > 0 else 0
    
    context = {
        'total_posts': total_posts,
        'published_posts': published_posts,
        'draft_posts': draft_posts,
        'published_percentage': published_percentage,
        'draft_percentage': draft_percentage,
        'total_views': total_views,
        'recent_posts': recent_posts,
        'popular_posts': popular_posts,
        'total_comments': total_comments,
        'pending_comments': pending_comments,
    }
    
    return render(request, 'blog/blog_analytics.html', context)

# Comment Management Views
@ensure_csrf_cookie
@login_required
@user_passes_test(is_admin_or_staff)
def comment_list(request):
    """List all comments with filtering options"""
    comments = Comment.objects.all().order_by('-created_at')
    
    # Filter by status
    status_filter = request.GET.get('status')
    if status_filter:
        comments = comments.filter(status=status_filter)
    
    # Search functionality
    search = request.GET.get('search')
    if search:
        comments = comments.filter(
            Q(name__icontains=search) |
            Q(email__icontains=search) |
            Q(content__icontains=search) |
            Q(post__title__icontains=search)
        )
    
    # Pagination
    paginator = Paginator(comments, 20)
    page_number = request.GET.get('page')
    comments = paginator.get_page(page_number)
    
    # Statistics
    pending_count = Comment.objects.filter(status='pending').count()
    approved_count = Comment.objects.filter(status='approved').count()
    spam_count = Comment.objects.filter(status='spam').count()
    
    context = {
        'comments': comments,
        'status_filter': status_filter,
        'search': search,
        'pending_count': pending_count,
        'approved_count': approved_count,
        'spam_count': spam_count,
    }
    
    return render(request, 'blog/comment_list.html', context)

@login_required
@user_passes_test(is_admin_or_staff)
@require_POST
def comment_approve(request, comment_id):
    """Approve a comment"""
    comment = get_object_or_404(Comment, id=comment_id)
    comment.status = 'approved'
    comment.save()
    messages.success(request, f'Comment by {comment.name} has been approved.')
    return redirect(request.META.get('HTTP_REFERER', 'conference:comment_list'))

@login_required
@user_passes_test(is_admin_or_staff)
@require_POST
def comment_reject(request, comment_id):
    """Reject/mark comment as spam"""
    comment = get_object_or_404(Comment, id=comment_id)
    comment.status = 'spam'
    comment.save()
    messages.success(request, f'Comment by {comment.name} has been marked as spam.')
    return redirect(request.META.get('HTTP_REFERER', 'conference:comment_list'))

@login_required
@user_passes_test(is_admin_or_staff)
@require_POST
def comment_delete(request, comment_id):
    """Delete a comment permanently"""
    comment = get_object_or_404(Comment, id=comment_id)
    name = comment.name
    comment.delete()
    messages.success(request, f'Comment by {name} has been deleted permanently.')
    return redirect(request.META.get('HTTP_REFERER', 'conference:comment_list'))

@login_required
@user_passes_test(is_admin_or_staff)
@require_POST
def comment_bulk_action(request):
    """Handle bulk actions on comments"""
    action = request.POST.get('action')
    selected_ids = request.POST.getlist('selected_comments')
    
    if not selected_ids:
        messages.error(request, 'No comments selected.')
        return redirect('conference:comment_list')
    
    comments = Comment.objects.filter(id__in=selected_ids)
    count = comments.count()
    
    if action == 'approve':
        comments.update(status='approved')
        messages.success(request, f'{count} comment{"s" if count != 1 else ""} approved.')
    elif action == 'spam':
        comments.update(status='spam')
        messages.success(request, f'{count} comment{"s" if count != 1 else ""} marked as spam.')
    elif action == 'delete':
        comments.delete()
        messages.success(request, f'{count} comment{"s" if count != 1 else ""} deleted permanently.')
    
    return redirect('conference:comment_list')

# Maintenance Mode Management
@ensure_csrf_cookie
@login_required
@user_passes_test(is_admin_or_staff)
def maintenance_list(request):
    """List maintenance mode configurations"""
    maintenances = MaintenanceMode.objects.all().order_by('-created_at')
    
    # Filter by status
    status_filter = request.GET.get('status')
    if status_filter == 'active':
        maintenances = maintenances.filter(is_active=True)
    elif status_filter == 'inactive':
        maintenances = maintenances.filter(is_active=False)
    
    context = {
        'maintenances': maintenances,
        'status_filter': status_filter,
    }
    
    return render(request, 'admin/maintenance_list.html', context)

@ensure_csrf_cookie
@login_required
@user_passes_test(is_admin_or_staff)
def maintenance_create(request):
    """Create new maintenance mode"""
    if request.method == 'POST':
        title = request.POST.get('title')
        message = request.POST.get('message')
        maintenance_type = request.POST.get('maintenance_type')
        page_url = request.POST.get('page_url', '')
        is_active = request.POST.get('is_active') == 'on'
        start_time = request.POST.get('start_time')
        end_time = request.POST.get('end_time')
        
        maintenance = MaintenanceMode.objects.create(
            title=title,
            message=message,
            maintenance_type=maintenance_type,
            page_url=page_url,
            is_active=is_active,
            start_time=start_time if start_time else None,
            end_time=end_time if end_time else None,
            created_by=request.user
        )
        
        messages.success(request, f'Maintenance mode "{title}" created successfully!')
        return redirect('conference:maintenance_list')
    
    return render(request, 'admin/maintenance_create.html')

@ensure_csrf_cookie
@login_required
@user_passes_test(is_admin_or_staff)
def maintenance_toggle(request, pk):
    """Toggle maintenance mode on/off"""
    maintenance = get_object_or_404(MaintenanceMode, pk=pk)
    maintenance.is_active = not maintenance.is_active
    maintenance.save()
    
    status = "activated" if maintenance.is_active else "deactivated"
    messages.success(request, f'Maintenance mode "{maintenance.title}" {status}!')
    
    return redirect('conference:maintenance_list')

# Notice Management  
@ensure_csrf_cookie
@login_required
@user_passes_test(is_admin_or_staff)
def notice_list(request):
    """List all notices"""
    notices = Notice.objects.all().order_by('-is_urgent', '-created_at')
    
    # Filter by status
    status_filter = request.GET.get('status')
    if status_filter == 'active':
        notices = notices.filter(is_active=True)
    elif status_filter == 'inactive':
        notices = notices.filter(is_active=False)
    
    context = {
        'notices': notices,
        'status_filter': status_filter,
    }
    
    return render(request, 'admin/notice_list.html', context)

@ensure_csrf_cookie
@login_required
@user_passes_test(is_admin_or_staff)
def notice_create(request):
    """Create new notice"""
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        notice_type = request.POST.get('notice_type')
        is_active = request.POST.get('is_active') == 'on'
        is_urgent = request.POST.get('is_urgent') == 'on'
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        show_on_pages = request.POST.get('show_on_pages', '')
        
        notice = Notice.objects.create(
            title=title,
            content=content,
            notice_type=notice_type,
            is_active=is_active,
            is_urgent=is_urgent,
            start_date=start_date if start_date else timezone.now(),
            end_date=end_date if end_date else None,
            show_on_pages=show_on_pages,
            created_by=request.user
        )
        
        messages.success(request, f'Notice "{title}" created successfully!')
        return redirect('conference:notice_list')
    
    return render(request, 'admin/notice_create.html')

@login_required
@user_passes_test(is_admin_or_staff)
@require_POST
def notice_toggle(request, pk):
    """Toggle notice on/off"""
    notice = get_object_or_404(Notice, pk=pk)
    notice.is_active = not notice.is_active
    notice.save()
    
    status = "activated" if notice.is_active else "deactivated"
    messages.success(request, f'Notice "{notice.title}" {status}!')
    
    return redirect('conference:notice_list')

@login_required
@user_passes_test(is_admin_or_staff)
@require_POST
def notice_delete(request, pk):
    """Delete notice"""
    notice = get_object_or_404(Notice, pk=pk)
    title = notice.title
    notice.delete()
    
    messages.success(request, f'Notice "{title}" deleted successfully!')
    return redirect('conference:notice_list')

# Admin Dashboard Views
@login_required
@user_passes_test(is_admin_or_staff)
def admin_dashboard(request):
    """Main admin dashboard with overview and quick access"""
    from django.utils import timezone
    from django.contrib.admin.models import LogEntry
    from django.contrib.contenttypes.models import ContentType
    from .models import BlogPost, Comment, Notice, MaintenanceMode, Timeline, StatusUpdate, Speaker, CommitteeMember, Schedule, UserProfile
    
    # Get or create user profile
    profile, created = UserProfile.objects.get_or_create(user=request.user)
    
    # Get statistics
    stats = {
        'blog_posts': BlogPost.objects.count(),
        'pending_comments': Comment.objects.filter(status='pending').count(),
        'active_notices': Notice.objects.filter(is_active=True).count(),
        'maintenance_modes': MaintenanceMode.objects.filter(is_active=True).count(),
        'speakers': Speaker.objects.count(),
        'committee_members': CommitteeMember.objects.count(),
        'timeline_items': Timeline.objects.count(),
        'status_updates': StatusUpdate.objects.count(),
        'schedule_items': Schedule.objects.count(),
    }
    
    # Get recent activities from Django admin logs
    recent_logs = LogEntry.objects.select_related('user', 'content_type').order_by('-action_time')[:10]
    
    recent_activities = []
    for log in recent_logs:
        activity = {
            'title': f'{log.get_action_flag_display()} {log.content_type.name if log.content_type else "item"}: {log.object_repr}',
            'timestamp': log.action_time,
            'user': log.user.username if log.user else 'System',
            'icon': get_activity_icon(log),
            'action': log.get_action_flag_display(),
            'object_type': log.content_type.name if log.content_type else 'Unknown',
        }
        recent_activities.append(activity)
    
    context = {
        'stats': stats,
        'recent_activities': recent_activities,
        'current_date': timezone.now(),
        'user_profile': profile,
    }
    return render(request, 'admin/dashboard.html', context)

def get_activity_icon(log_entry):
    """Get appropriate icon for activity based on content type and action"""
    if not log_entry.content_type:
        return 'fa-cog'
    
    model_name = log_entry.content_type.model.lower()
    action_flag = log_entry.action_flag
    
    # Action-based icons
    if action_flag == 1:  # Addition
        return 'fa-plus-circle'
    elif action_flag == 2:  # Change
        return 'fa-edit'
    elif action_flag == 3:  # Deletion
        return 'fa-trash'
    
    # Model-specific icons
    icon_map = {
        'blogpost': 'fa-blog',
        'comment': 'fa-comment',
        'notice': 'fa-bullhorn',
        'speaker': 'fa-microphone',
        'committeemember': 'fa-users',
        'timeline': 'fa-calendar',
        'statusupdate': 'fa-broadcast-tower',
        'schedule': 'fa-calendar-week',
        'maintenancemode': 'fa-tools',
        'user': 'fa-user',
    }
    
    return icon_map.get(model_name, 'fa-cog')

# User Management Views
@login_required
@user_passes_test(lambda u: u.is_superuser or (hasattr(u, 'profile') and u.profile.has_permission('can_manage_users')))
def user_management(request):
    """User management dashboard"""
    from django.contrib.auth.models import User
    from .models import AdminRole, UserProfile
    
    users = User.objects.select_related('profile', 'profile__admin_role').order_by('-date_joined')
    admin_roles = AdminRole.objects.filter(is_active=True).order_by('name')
    
    # Get statistics
    stats = {
        'total_users': users.count(),
        'admin_users': users.filter(profile__is_admin_user=True).count(),
        'superusers': users.filter(is_superuser=True).count(),
        'active_users': users.filter(is_active=True).count(),
        'inactive_users': users.filter(is_active=False).count(),
    }
    
    context = {
        'users': users,
        'admin_roles': admin_roles,
        'stats': stats,
    }
    return render(request, 'admin/user_management.html', context)

@login_required
@user_passes_test(lambda u: u.is_superuser or (hasattr(u, 'profile') and u.profile.has_permission('can_manage_users')))
def user_create(request):
    """Create new admin user"""
    from django.contrib.auth.models import User
    from .models import AdminRole, UserProfile
    
    if request.method == 'POST':
        # Get form data
        username = request.POST.get('username')
        email = request.POST.get('email')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        password = request.POST.get('password')
        admin_role_id = request.POST.get('admin_role')
        is_admin_user = request.POST.get('is_admin_user') == 'on'
        is_staff = request.POST.get('is_staff') == 'on'
        
        # Additional profile fields
        phone = request.POST.get('phone')
        department = request.POST.get('department')
        position = request.POST.get('position')
        bio = request.POST.get('bio')
        
        try:
            # Check if username already exists
            if User.objects.filter(username=username).exists():
                messages.error(request, f'Username "{username}" already exists.')
                return redirect('conference:user_create')
            
            # Create user
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password,
                first_name=first_name,
                last_name=last_name,
                is_staff=is_staff
            )
            
            # Get admin role
            admin_role = None
            if admin_role_id:
                admin_role = AdminRole.objects.get(id=admin_role_id)
            
            # Create user profile
            profile = UserProfile.objects.create(
                user=user,
                admin_role=admin_role,
                is_admin_user=is_admin_user,
                phone=phone,
                department=department,
                position=position,
                bio=bio
            )
            
            # Handle avatar upload
            if 'avatar' in request.FILES:
                profile.avatar = request.FILES['avatar']
                profile.save()
            
            messages.success(request, f'User "{user.get_full_name() or user.username}" created successfully!')
            return redirect('conference:user_management')
            
        except Exception as e:
            messages.error(request, f'Error creating user: {str(e)}')
            return redirect('conference:user_create')
    
    admin_roles = AdminRole.objects.filter(is_active=True).order_by('name')
    context = {
        'admin_roles': admin_roles,
    }
    return render(request, 'admin/user_create.html', context)

@login_required
@user_passes_test(lambda u: u.is_superuser or (hasattr(u, 'profile') and u.profile.has_permission('can_manage_users')))
def user_edit(request, user_id):
    """Edit user details and permissions"""
    from django.contrib.auth.models import User
    from .models import AdminRole, UserProfile
    
    user = get_object_or_404(User, id=user_id)
    
    # Prevent non-superusers from editing superusers
    if user.is_superuser and not request.user.is_superuser:
        messages.error(request, 'You cannot edit superuser accounts.')
        return redirect('conference:user_management')
    
    # Get or create user profile
    profile, created = UserProfile.objects.get_or_create(user=user)
    
    if request.method == 'POST':
        # Update user data
        user.first_name = request.POST.get('first_name')
        user.last_name = request.POST.get('last_name')
        user.email = request.POST.get('email')
        user.is_active = request.POST.get('is_active') == 'on'
        
        # Only allow superusers to change staff/superuser status
        if request.user.is_superuser:
            user.is_staff = request.POST.get('is_staff') == 'on'
            user.is_superuser = request.POST.get('is_superuser') == 'on'
        
        # Update password if provided
        new_password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        
        if new_password:
            if new_password == confirm_password:
                if len(new_password) >= 8:
                    user.set_password(new_password)
                    messages.success(request, 'Password updated successfully!')
                    
                    # Force password change on next login if requested
                    if request.POST.get('force_password_change') == 'on':
                        # You can implement this with a custom field in UserProfile
                        # profile.force_password_change = True
                        messages.info(request, 'User will be required to change password on next login.')
                else:
                    messages.error(request, 'Password must be at least 8 characters long.')
                    return render(request, 'admin/user_edit.html', {
                        'edit_user': user,
                        'profile': profile,
                        'admin_roles': AdminRole.objects.filter(is_active=True).order_by('name'),
                    })
            else:
                messages.error(request, 'Passwords do not match.')
                return render(request, 'admin/user_edit.html', {
                    'edit_user': user,
                    'profile': profile,
                    'admin_roles': AdminRole.objects.filter(is_active=True).order_by('name'),
                })
        
        user.save()
        
        # Update profile
        admin_role_id = request.POST.get('admin_role')
        if admin_role_id:
            profile.admin_role = AdminRole.objects.get(id=admin_role_id)
        else:
            profile.admin_role = None
            
        profile.is_admin_user = request.POST.get('is_admin_user') == 'on'
        profile.phone = request.POST.get('phone')
        profile.department = request.POST.get('department')
        profile.position = request.POST.get('position')
        profile.bio = request.POST.get('bio')
        
        # Handle avatar upload
        if 'avatar' in request.FILES:
            profile.avatar = request.FILES['avatar']
        
        profile.save()
        
        messages.success(request, f'User "{user.get_full_name() or user.username}" updated successfully!')
        return redirect('conference:user_management')
    
    admin_roles = AdminRole.objects.filter(is_active=True).order_by('name')
    context = {
        'edit_user': user,
        'profile': profile,
        'admin_roles': admin_roles,
    }
    return render(request, 'admin/user_edit.html', context)

@login_required
@user_passes_test(lambda u: u.is_superuser or (hasattr(u, 'profile') and u.profile.has_permission('can_manage_users')))
def user_delete(request, user_id):
    """Delete user (only for superusers)"""
    if not request.user.is_superuser:
        messages.error(request, 'Only superusers can delete users.')
        return redirect('conference:user_management')
    
    user = get_object_or_404(User, id=user_id)
    
    # Prevent deletion of current user and other superusers
    if user == request.user:
        messages.error(request, 'You cannot delete your own account.')
        return redirect('conference:user_management')
    
    if user.is_superuser:
        messages.error(request, 'Cannot delete superuser accounts.')
        return redirect('conference:user_management')
    
    if request.method == 'POST':
        username = user.username
        user.delete()
        messages.success(request, f'User "{username}" deleted successfully!')
    
    return redirect('conference:user_management')

@login_required
@user_passes_test(lambda u: u.is_superuser or (hasattr(u, 'profile') and u.profile.has_permission('can_manage_users')))
def role_management(request):
    """Manage admin roles and permissions"""
    from .models import AdminRole
    
    roles = AdminRole.objects.all().order_by('name')
    
    context = {
        'roles': roles,
    }
    return render(request, 'admin/role_management.html', context)

@login_required
@user_passes_test(lambda u: u.is_superuser)
def role_create(request):
    """Create new admin role (superuser only)"""
    from .models import AdminRole
    
    if request.method == 'POST':
        name = request.POST.get('name')
        role_type = request.POST.get('role_type')
        description = request.POST.get('description')
        
        # Get permissions
        permissions = {
            'can_access_dashboard': request.POST.get('can_access_dashboard') == 'on',
            'can_manage_users': request.POST.get('can_manage_users') == 'on',
            'can_manage_content': request.POST.get('can_manage_content') == 'on',
            'can_manage_blog': request.POST.get('can_manage_blog') == 'on',
            'can_manage_events': request.POST.get('can_manage_events') == 'on',
            'can_manage_schedule': request.POST.get('can_manage_schedule') == 'on',
            'can_manage_speakers': request.POST.get('can_manage_speakers') == 'on',
            'can_manage_committee': request.POST.get('can_manage_committee') == 'on',
            'can_manage_notices': request.POST.get('can_manage_notices') == 'on',
            'can_manage_timeline': request.POST.get('can_manage_timeline') == 'on',
            'can_export_data': request.POST.get('can_export_data') == 'on',
            'can_view_logs': request.POST.get('can_view_logs') == 'on',
        }
        
        try:
            role = AdminRole.objects.create(
                name=name,
                role_type=role_type,
                description=description,
                **permissions
            )
            messages.success(request, f'Role "{role.name}" created successfully!')
            return redirect('conference:role_management')
        except Exception as e:
            messages.error(request, f'Error creating role: {str(e)}')
    
    return render(request, 'admin/role_create.html')

def has_admin_permission(user, permission):
    """Check if user has specific admin permission"""
    if user.is_superuser:
        return True
    if not hasattr(user, 'profile') or not user.profile.is_admin_user:
        return False
    return user.profile.has_permission(permission)

# Timeline Management Views
@login_required
@user_passes_test(is_admin_or_staff)
def timeline_list(request):
    """List all timeline items"""
    from .models import Timeline
    
    timelines = Timeline.objects.all()
    
    # Filter options
    status_filter = request.GET.get('status')
    type_filter = request.GET.get('type')
    
    if status_filter:
        timelines = timelines.filter(status=status_filter)
    if type_filter:
        timelines = timelines.filter(timeline_type=type_filter)
    
    context = {
        'timelines': timelines,
        'status_choices': Timeline.STATUS_CHOICES,
        'type_choices': Timeline.TIMELINE_TYPES,
        'current_status': status_filter,
        'current_type': type_filter,
    }
    return render(request, 'admin/timeline_list.html', context)

@login_required
@user_passes_test(is_admin_or_staff)
def timeline_create(request):
    """Create new timeline item"""
    from .models import Timeline
    
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        timeline_type = request.POST.get('timeline_type')
        status = request.POST.get('status')
        date = request.POST.get('date')
        end_date = request.POST.get('end_date')
        is_featured = request.POST.get('is_featured') == 'on'
        is_public = request.POST.get('is_public') == 'on'
        icon = request.POST.get('icon')
        color = request.POST.get('color')
        
        timeline = Timeline.objects.create(
            title=title,
            description=description,
            timeline_type=timeline_type,
            status=status,
            date=date,
            end_date=end_date if end_date else None,
            is_featured=is_featured,
            is_public=is_public,
            icon=icon,
            color=color,
            created_by=request.user
        )
        
        messages.success(request, f'Timeline item "{timeline.title}" created successfully!')
        return redirect('conference:timeline_list')
    
    context = {
        'status_choices': Timeline.STATUS_CHOICES,
        'type_choices': Timeline.TIMELINE_TYPES,
    }
    return render(request, 'admin/timeline_create.html', context)

@login_required
@user_passes_test(is_admin_or_staff)
def timeline_edit(request, pk):
    """Edit timeline item"""
    from .models import Timeline
    
    timeline = get_object_or_404(Timeline, pk=pk)
    
    if request.method == 'POST':
        timeline.title = request.POST.get('title')
        timeline.description = request.POST.get('description')
        timeline.timeline_type = request.POST.get('timeline_type')
        timeline.status = request.POST.get('status')
        timeline.date = request.POST.get('date')
        timeline.end_date = request.POST.get('end_date') if request.POST.get('end_date') else None
        timeline.is_featured = request.POST.get('is_featured') == 'on'
        timeline.is_public = request.POST.get('is_public') == 'on'
        timeline.icon = request.POST.get('icon')
        timeline.color = request.POST.get('color')
        timeline.save()
        
        messages.success(request, f'Timeline item "{timeline.title}" updated successfully!')
        return redirect('conference:timeline_list')
    
    context = {
        'timeline': timeline,
        'status_choices': Timeline.STATUS_CHOICES,
        'type_choices': Timeline.TIMELINE_TYPES,
    }
    return render(request, 'admin/timeline_edit.html', context)

@login_required
@user_passes_test(is_admin_or_staff)
@require_POST
def timeline_delete(request, pk):
    """Delete timeline item"""
    from .models import Timeline
    
    timeline = get_object_or_404(Timeline, pk=pk)
    title = timeline.title
    timeline.delete()
    
    messages.success(request, f'Timeline item "{title}" deleted successfully!')
    return redirect('conference:timeline_list')

# Status Update Management Views
@login_required
@user_passes_test(is_admin_or_staff)
def status_update_list(request):
    """List all status updates"""
    from .models import StatusUpdate
    
    updates = StatusUpdate.objects.all()
    
    # Filter options
    type_filter = request.GET.get('type')
    priority_filter = request.GET.get('priority')
    
    if type_filter:
        updates = updates.filter(update_type=type_filter)
    if priority_filter:
        updates = updates.filter(priority=priority_filter)
    
    context = {
        'updates': updates,
        'type_choices': StatusUpdate.UPDATE_TYPES,
        'priority_choices': StatusUpdate.PRIORITY_LEVELS,
        'current_type': type_filter,
        'current_priority': priority_filter,
    }
    return render(request, 'admin/status_update_list.html', context)

@login_required
@user_passes_test(is_admin_or_staff)
def status_update_create(request):
    """Create new status update"""
    from .models import StatusUpdate, Timeline
    
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        update_type = request.POST.get('update_type')
        priority = request.POST.get('priority')
        is_published = request.POST.get('is_published') == 'on'
        is_featured = request.POST.get('is_featured') == 'on'
        publish_date = request.POST.get('publish_date')
        expire_date = request.POST.get('expire_date')
        related_timeline_id = request.POST.get('related_timeline')
        tags = request.POST.get('tags')
        
        update = StatusUpdate.objects.create(
            title=title,
            content=content,
            update_type=update_type,
            priority=priority,
            is_published=is_published,
            is_featured=is_featured,
            publish_date=publish_date,
            expire_date=expire_date if expire_date else None,
            related_timeline_id=related_timeline_id if related_timeline_id else None,
            tags=tags,
            created_by=request.user
        )
        
        messages.success(request, f'Status update "{update.title}" created successfully!')
        return redirect('conference:status_update_list')
    
    context = {
        'type_choices': StatusUpdate.UPDATE_TYPES,
        'priority_choices': StatusUpdate.PRIORITY_LEVELS,
        'timelines': Timeline.objects.all().order_by('date'),
    }
    return render(request, 'admin/status_update_create.html', context)

@login_required
@user_passes_test(is_admin_or_staff)
def status_update_edit(request, pk):
    """Edit status update"""
    from .models import StatusUpdate, Timeline
    
    update = get_object_or_404(StatusUpdate, pk=pk)
    
    if request.method == 'POST':
        update.title = request.POST.get('title')
        update.content = request.POST.get('content')
        update.update_type = request.POST.get('update_type')
        update.priority = request.POST.get('priority')
        update.is_published = request.POST.get('is_published') == 'on'
        update.is_featured = request.POST.get('is_featured') == 'on'
        update.publish_date = request.POST.get('publish_date')
        update.expire_date = request.POST.get('expire_date') if request.POST.get('expire_date') else None
        update.related_timeline_id = request.POST.get('related_timeline') if request.POST.get('related_timeline') else None
        update.tags = request.POST.get('tags')
        update.save()
        
        messages.success(request, f'Status update "{update.title}" updated successfully!')
        return redirect('conference:status_update_list')
    
    context = {
        'update': update,
        'type_choices': StatusUpdate.UPDATE_TYPES,
        'priority_choices': StatusUpdate.PRIORITY_LEVELS,
        'timelines': Timeline.objects.all().order_by('date'),
    }
    return render(request, 'admin/status_update_edit.html', context)

@login_required
@user_passes_test(is_admin_or_staff)
@require_POST
def status_update_delete(request, pk):
    """Delete status update"""
    from .models import StatusUpdate
    
    update = get_object_or_404(StatusUpdate, pk=pk)
    title = update.title
    update.delete()
    
    messages.success(request, f'Status update "{title}" deleted successfully!')
    return redirect('conference:status_update_list')

@login_required
@user_passes_test(is_admin_or_staff)
@require_POST
def status_update_toggle(request, pk):
    """Toggle status update published status"""
    from .models import StatusUpdate
    
    update = get_object_or_404(StatusUpdate, pk=pk)
    update.is_published = not update.is_published
    update.save()
    
    status = 'published' if update.is_published else 'unpublished'
    messages.success(request, f'Status update "{update.title}" {status} successfully!')
    return redirect('conference:status_update_list')

# Schedule Management Views
@login_required
@user_passes_test(is_admin_or_staff)
def schedule_list(request):
    """List all schedule items"""
    from .models import Schedule
    from django.utils import timezone
    
    schedules = Schedule.objects.all().order_by('date', 'start_time')
    
    # Filter options
    day_filter = request.GET.get('day')
    type_filter = request.GET.get('type')
    
    if day_filter:
        schedules = schedules.filter(day=day_filter)
    if type_filter:
        schedules = schedules.filter(schedule_type=type_filter)
    
    # Calculate statistics
    total_sessions = Schedule.objects.count()
    active_sessions = Schedule.objects.filter(is_published=True).count()
    schedule_days = Schedule.objects.values('date').distinct().count()
    
    # Get upcoming sessions (future dates)
    current_time = timezone.now()
    upcoming_sessions = Schedule.objects.filter(
        date__gte=current_time.date()
    ).count()
    
    context = {
        'schedule_items': schedules,  # Changed from schedules to schedule_items
        'total_sessions': total_sessions,
        'active_sessions': active_sessions,
        'schedule_days': schedule_days,
        'upcoming_sessions': upcoming_sessions,
        'type_choices': Schedule.SCHEDULE_TYPES,
        'current_day': day_filter,
        'current_type': type_filter,
    }
    return render(request, 'admin/schedule_list.html', context)

@login_required
@user_passes_test(is_admin_or_staff)
def schedule_create(request):
    """Create new schedule item"""
    from .models import Schedule
    from django.contrib.auth.models import User
    
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        schedule_type = request.POST.get('schedule_type')
        speaker = request.POST.get('speaker')
        venue = request.POST.get('venue')  # This will map to location field
        day = request.POST.get('day')
        start_time = request.POST.get('start_time')
        end_time = request.POST.get('end_time')
        date = request.POST.get('date')
        is_active = request.POST.get('is_active') == 'on'
        
        # Get current user
        current_user = request.user
        
        schedule = Schedule.objects.create(
            title=title,
            description=description,
            schedule_type=schedule_type,
            speaker=speaker or '',
            location=venue or '',  # Map venue to location
            day=day,
            start_time=start_time,
            end_time=end_time or start_time,  # Use start_time if end_time not provided
            date=date,
            is_published=is_active,  # Map is_active to is_published
            created_by=current_user
        )
        
        messages.success(request, f'Schedule session "{title}" created successfully!')
        return redirect('conference:schedule_list')
    
    context = {
        'type_choices': Schedule.SCHEDULE_TYPES,
        'day_choices': Schedule.DAYS,
    }
    return render(request, 'admin/schedule_create.html', context)

@login_required
@user_passes_test(is_admin_or_staff)
def schedule_edit(request, pk):
    """Edit schedule item"""
    from .models import Schedule
    
    schedule = get_object_or_404(Schedule, pk=pk)
    
    if request.method == 'POST':
        schedule.title = request.POST.get('title')
        schedule.description = request.POST.get('description')
        schedule.schedule_type = request.POST.get('schedule_type')
        schedule.speaker = request.POST.get('speaker') or ''
        schedule.location = request.POST.get('venue') or ''  # Map venue to location
        schedule.day = request.POST.get('day')
        schedule.start_time = request.POST.get('start_time')
        schedule.end_time = request.POST.get('end_time') or schedule.start_time
        schedule.date = request.POST.get('date')
        schedule.is_published = request.POST.get('is_active') == 'on'  # Map is_active to is_published
        schedule.save()
        
        messages.success(request, f'Schedule session "{schedule.title}" updated successfully!')
        return redirect('conference:schedule_list')
    
    context = {
        'schedule': schedule,
        'type_choices': Schedule.SCHEDULE_TYPES,
        'day_choices': Schedule.DAYS,
    }
    return render(request, 'admin/schedule_edit.html', context)

@login_required
@user_passes_test(is_admin_or_staff)
@require_POST
def schedule_delete(request, pk):
    """Delete schedule item"""
    from .models import Schedule
    
    schedule = get_object_or_404(Schedule, pk=pk)
    title = schedule.title
    schedule.delete()
    
    messages.success(request, f'Schedule item "{title}" deleted successfully!')
    return redirect('conference:schedule_list')

@login_required
@user_passes_test(is_admin_or_staff)
@require_POST
def schedule_toggle(request, pk):
    """Toggle schedule item published status"""
    from .models import Schedule
    
    schedule = get_object_or_404(Schedule, pk=pk)
    schedule.is_published = not schedule.is_published
    schedule.save()
    
    status = 'published' if schedule.is_published else 'unpublished'
    messages.success(request, f'Schedule item "{schedule.title}" {status} successfully!')
    return redirect('conference:schedule_list')

# Speaker Management Views
@login_required
@user_passes_test(is_admin_or_staff)
def speaker_list(request):
    """List all speakers"""
    from .models import Speaker
    
    speakers = Speaker.objects.all()
    
    # Filter options
    type_filter = request.GET.get('type')
    status_filter = request.GET.get('status')
    
    if type_filter:
        speakers = speakers.filter(speaker_type=type_filter)
    if status_filter == 'published':
        speakers = speakers.filter(is_published=True)
    elif status_filter == 'unpublished':
        speakers = speakers.filter(is_published=False)
    
    # Calculate statistics
    total_speakers = Speaker.objects.count()
    published_speakers = Speaker.objects.filter(is_published=True).count()
    keynote_speakers = Speaker.objects.filter(speaker_type='keynote').count()
    invited_speakers = Speaker.objects.filter(speaker_type='invited').count()
    
    context = {
        'speakers': speakers,
        'total_speakers': total_speakers,
        'published_speakers': published_speakers,
        'keynote_speakers': keynote_speakers,
        'invited_speakers': invited_speakers,
        'type_choices': Speaker.SPEAKER_TYPES,
        'current_type': type_filter,
        'current_status': status_filter,
    }
    return render(request, 'admin/speaker_list.html', context)

@login_required
@user_passes_test(is_admin_or_staff)
def speaker_create(request):
    """Create new speaker"""
    from .models import Speaker
    
    if request.method == 'POST':
        name = request.POST.get('name')
        title = request.POST.get('title')
        organization = request.POST.get('organization')
        country = request.POST.get('country')
        bio = request.POST.get('bio')
        expertise = request.POST.get('expertise')
        speaker_type = request.POST.get('speaker_type')
        talk_title = request.POST.get('talk_title')
        talk_abstract = request.POST.get('talk_abstract')
        session_time = request.POST.get('session_time')
        email = request.POST.get('email')
        website = request.POST.get('website')
        linkedin = request.POST.get('linkedin')
        twitter = request.POST.get('twitter')
        orcid = request.POST.get('orcid')
        is_featured = request.POST.get('is_featured') == 'on'
        is_published = request.POST.get('is_published') == 'on'
        display_order = request.POST.get('display_order', 0)
        
        speaker = Speaker.objects.create(
            name=name,
            title=title,
            organization=organization,
            country=country,
            bio=bio,
            expertise=expertise,
            speaker_type=speaker_type,
            talk_title=talk_title,
            talk_abstract=talk_abstract,
            session_time=session_time,
            email=email,
            website=website,
            linkedin=linkedin,
            twitter=twitter,
            orcid=orcid,
            is_featured=is_featured,
            is_published=is_published,
            display_order=int(display_order) if display_order else 0,
            created_by=request.user
        )
        
        # Handle photo upload
        if 'photo' in request.FILES:
            speaker.photo = request.FILES['photo']
            speaker.save()
        
        messages.success(request, f'Speaker "{speaker.name}" created successfully!')
        return redirect('conference:speaker_list')
    
    context = {
        'type_choices': Speaker.SPEAKER_TYPES,
    }
    return render(request, 'admin/speaker_create.html', context)

@login_required
@user_passes_test(is_admin_or_staff)
def speaker_edit(request, pk):
    """Edit speaker"""
    from .models import Speaker
    
    speaker = get_object_or_404(Speaker, pk=pk)
    
    if request.method == 'POST':
        speaker.name = request.POST.get('name')
        speaker.title = request.POST.get('title')
        speaker.organization = request.POST.get('organization')
        speaker.country = request.POST.get('country')
        speaker.bio = request.POST.get('bio')
        speaker.expertise = request.POST.get('expertise')
        speaker.speaker_type = request.POST.get('speaker_type')
        speaker.talk_title = request.POST.get('talk_title')
        speaker.talk_abstract = request.POST.get('talk_abstract')
        speaker.session_time = request.POST.get('session_time')
        speaker.email = request.POST.get('email')
        speaker.website = request.POST.get('website')
        speaker.linkedin = request.POST.get('linkedin')
        speaker.twitter = request.POST.get('twitter')
        speaker.orcid = request.POST.get('orcid')
        speaker.is_featured = request.POST.get('is_featured') == 'on'
        speaker.is_published = request.POST.get('is_published') == 'on'
        speaker.display_order = int(request.POST.get('display_order', 0)) if request.POST.get('display_order') else 0
        
        # Handle photo upload
        if 'photo' in request.FILES:
            speaker.photo = request.FILES['photo']
        
        speaker.save()
        
        messages.success(request, f'Speaker "{speaker.name}" updated successfully!')
        return redirect('conference:speaker_list')
    
    context = {
        'speaker': speaker,
        'type_choices': Speaker.SPEAKER_TYPES,
    }
    return render(request, 'admin/speaker_edit.html', context)

@login_required
@user_passes_test(is_admin_or_staff)
@require_POST
def speaker_delete(request, pk):
    """Delete speaker"""
    from .models import Speaker
    
    speaker = get_object_or_404(Speaker, pk=pk)
    name = speaker.name
    speaker.delete()
    
    messages.success(request, f'Speaker "{name}" deleted successfully!')
    return redirect('conference:speaker_list')

@login_required
@user_passes_test(is_admin_or_staff)
@require_POST
def speaker_toggle(request, pk):
    """Toggle speaker published status"""
    from .models import Speaker
    
    speaker = get_object_or_404(Speaker, pk=pk)
    speaker.is_published = not speaker.is_published
    speaker.save()
    
    status = 'published' if speaker.is_published else 'unpublished'
    messages.success(request, f'Speaker "{speaker.name}" {status} successfully!')
    return redirect('conference:speaker_list')


# Committee Management Views
@login_required
@user_passes_test(is_admin_or_staff)
def committee_list(request):
    """List all committee members"""
    from .models import CommitteeMember
    
    committee_members = CommitteeMember.objects.all()
    
    context = {
        'committee_members': committee_members,
        'total_members': committee_members.count(),
    }
    return render(request, 'admin/committee_list.html', context)

@login_required
@user_passes_test(is_admin_or_staff)
def committee_create(request):
    """Create new committee member"""
    from .models import CommitteeMember
    
    if request.method == 'POST':
        name = request.POST.get('name')
        title = request.POST.get('title')
        organization = request.POST.get('organization')
        order = request.POST.get('order', 0)
        role = request.POST.get('role')
        hierarchy_level = request.POST.get('hierarchy_level')
        email = request.POST.get('email', '')
        phone = request.POST.get('phone', '')
        bio = request.POST.get('bio', '')
        image = request.FILES.get('image')
        is_active = request.POST.get('is_active', 'on') == 'on'
        
        committee_member = CommitteeMember.objects.create(
            name=name,
            title=title,
            organization=organization,
            order=int(order) if order else 0,
            role=role,
            hierarchy_level=int(hierarchy_level),
            email=email,
            phone=phone,
            bio=bio,
            image=image,
            is_active=is_active
        )
        
        messages.success(request, f'Committee member "{name}" created successfully!')
        return redirect('conference:committee_list')
    
    context = {
        'next_order': CommitteeMember.objects.count() + 1,
        'role_choices': CommitteeMember.ROLE_CHOICES,
        'hierarchy_choices': CommitteeMember.HIERARCHY_LEVELS,
    }
    return render(request, 'admin/committee_create.html', context)

@login_required
@user_passes_test(is_admin_or_staff)
def committee_edit(request, pk):
    """Edit committee member"""
    from .models import CommitteeMember
    
    committee_member = get_object_or_404(CommitteeMember, pk=pk)
    
    if request.method == 'POST':
        committee_member.name = request.POST.get('name')
        committee_member.title = request.POST.get('title')
        committee_member.organization = request.POST.get('organization')
        committee_member.order = int(request.POST.get('order', 0)) if request.POST.get('order') else 0
        committee_member.role = request.POST.get('role')
        committee_member.hierarchy_level = int(request.POST.get('hierarchy_level'))
        committee_member.email = request.POST.get('email', '')
        committee_member.phone = request.POST.get('phone', '')
        committee_member.bio = request.POST.get('bio', '')
        committee_member.is_active = request.POST.get('is_active') == 'on'
        
        if request.FILES.get('image'):
            committee_member.image = request.FILES.get('image')
        
        committee_member.save()
        
        messages.success(request, f'Committee member "{committee_member.name}" updated successfully!')
        return redirect('conference:committee_list')
    
    context = {
        'committee_member': committee_member,
        'role_choices': CommitteeMember.ROLE_CHOICES,
        'hierarchy_choices': CommitteeMember.HIERARCHY_LEVELS,
    }
    return render(request, 'admin/committee_edit.html', context)

@login_required
@user_passes_test(is_admin_or_staff)
@require_POST
def committee_delete(request, pk):
    """Delete committee member"""
    from .models import CommitteeMember
    
    committee_member = get_object_or_404(CommitteeMember, pk=pk)
    name = committee_member.name
    committee_member.delete()
    
    messages.success(request, f'Committee member "{name}" deleted successfully!')
    return redirect('conference:committee_list')

@login_required
@user_passes_test(is_admin_or_staff)
@require_POST
def committee_reorder(request):
    """Reorder committee members"""
    from .models import CommitteeMember
    import json
    
    try:
        order_data = json.loads(request.body)
        for item in order_data:
            CommitteeMember.objects.filter(pk=item['id']).update(order=item['order'])
        
        messages.success(request, 'Committee member order updated successfully!')
        return JsonResponse({'status': 'success'})
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)})


# Custom error handlers
def custom_404_view(request, exception=None):
    """Custom 404 error page"""
    return render(request, 'errors/404.html', status=404)

def custom_500_view(request):
    """Custom 500 error page"""
    return render(request, 'errors/500.html', status=500)

def test_404(request):
    """Test 404 error page in development"""
    return render(request, 'errors/404.html', status=404)

def test_500(request):
    """Test 500 error page in development"""
    return render(request, 'errors/500.html', status=500)

# Export functionality
import csv
import json
from datetime import datetime
from django.http import HttpResponse
from django.contrib.admin.models import LogEntry
from django.contrib.contenttypes.models import ContentType
from io import BytesIO

@login_required
@user_passes_test(is_admin_or_staff)
def export_speakers(request):
    """Export speakers list in various formats"""
    export_format = request.GET.get('format', 'excel')
    from .models import Speaker
    
    speakers = Speaker.objects.all().order_by('display_order', 'name')
    
    if export_format == 'excel':
        return export_speakers_excel(speakers)
    elif export_format == 'pdf':
        return export_speakers_pdf(speakers)
    elif export_format == 'csv':
        return export_speakers_csv(speakers)
    elif export_format == 'json':
        return export_speakers_json(speakers)
    else:
        return HttpResponse("Invalid format", status=400)

@login_required
@user_passes_test(is_admin_or_staff)
def export_committee(request):
    """Export committee members list in various formats"""
    export_format = request.GET.get('format', 'excel')
    
    committee_members = CommitteeMember.objects.filter(is_active=True).order_by('hierarchy_level', 'name')
    
    if export_format == 'excel':
        return export_committee_excel(committee_members)
    elif export_format == 'pdf':
        return export_committee_pdf(committee_members)
    elif export_format == 'csv':
        return export_committee_csv(committee_members)
    elif export_format == 'json':
        return export_committee_json(committee_members)
    else:
        return HttpResponse("Invalid format", status=400)

@login_required
@user_passes_test(is_admin_or_staff)
def export_schedule(request):
    """Export schedule list in various formats"""
    export_format = request.GET.get('format', 'excel')
    from .models import Schedule
    
    schedules = Schedule.objects.all().order_by('date', 'start_time')
    
    if export_format == 'excel':
        return export_schedule_excel(schedules)
    elif export_format == 'pdf':
        return export_schedule_pdf(schedules)
    elif export_format == 'csv':
        return export_schedule_csv(schedules)
    elif export_format == 'json':
        return export_schedule_json(schedules)
    else:
        return HttpResponse("Invalid format", status=400)

@login_required
@user_passes_test(is_admin_or_staff)
def export_logs(request):
    """Export activity logs in various formats"""
    export_format = request.GET.get('format', 'excel')
    days = int(request.GET.get('days', 30))
    
    from datetime import timedelta
    cutoff_date = timezone.now() - timedelta(days=days)
    
    logs = LogEntry.objects.filter(
        action_time__gte=cutoff_date
    ).select_related('user', 'content_type').order_by('-action_time')
    
    if export_format == 'excel':
        return export_logs_excel(logs, days)
    elif export_format == 'pdf':
        return export_logs_pdf(logs, days)
    elif export_format == 'csv':
        return export_logs_csv(logs, days)
    elif export_format == 'json':
        return export_logs_json(logs, days)
    else:
        return HttpResponse("Invalid format", status=400)

def export_speakers_excel(speakers):
    """Export speakers to Excel format"""
    from openpyxl import Workbook
    from openpyxl.styles import Font, Alignment, PatternFill
    
    wb = Workbook()
    ws = wb.active
    ws.title = "Speakers List"
    
    # Header styling
    header_font = Font(bold=True, size=12)
    header_fill = PatternFill(start_color="366092", end_color="366092", fill_type="solid")
    
    # Headers
    headers = [
        'Name', 'Title', 'Organization', 'Country', 'Speaker Type', 
        'Talk Title', 'Session Time', 'Email', 'Website', 'LinkedIn',
        'Is Featured', 'Is Published', 'Created Date'
    ]
    
    for col, header in enumerate(headers, 1):
        cell = ws.cell(row=1, column=col, value=header)
        cell.font = header_font
        cell.fill = header_fill
        cell.alignment = Alignment(horizontal='center')
    
    # Data rows
    for row, speaker in enumerate(speakers, 2):
        ws.cell(row=row, column=1, value=speaker.name)
        ws.cell(row=row, column=2, value=speaker.title)
        ws.cell(row=row, column=3, value=speaker.organization)
        ws.cell(row=row, column=4, value=speaker.country)
        ws.cell(row=row, column=5, value=speaker.get_speaker_type_display())
        ws.cell(row=row, column=6, value=speaker.talk_title)
        ws.cell(row=row, column=7, value=speaker.session_time)
        ws.cell(row=row, column=8, value=speaker.email)
        ws.cell(row=row, column=9, value=speaker.website)
        ws.cell(row=row, column=10, value=speaker.linkedin)
        ws.cell(row=row, column=11, value='Yes' if speaker.is_featured else 'No')
        ws.cell(row=row, column=12, value='Yes' if speaker.is_published else 'No')
        ws.cell(row=row, column=13, value=speaker.created_at.strftime('%Y-%m-%d %H:%M'))
    
    # Adjust column widths
    for column in ws.columns:
        max_length = 0
        column_letter = column[0].column_letter
        for cell in column:
            try:
                if len(str(cell.value)) > max_length:
                    max_length = len(str(cell.value))
            except:
                pass
        adjusted_width = min(max_length + 2, 50)
        ws.column_dimensions[column_letter].width = adjusted_width
    
    # Create response
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = f'attachment; filename="speakers_list_{datetime.now().strftime("%Y%m%d_%H%M")}.xlsx"'
    
    wb.save(response)
    return response

def export_speakers_pdf(speakers):
    """Export speakers to PDF format"""
    from reportlab.lib.pagesizes import A4
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
    from reportlab.lib import colors
    
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4)
    styles = getSampleStyleSheet()
    story = []
    
    # Title
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Title'],
        fontSize=18,
        textColor=colors.darkblue,
        alignment=1
    )
    story.append(Paragraph(f"Conference Speakers List", title_style))
    story.append(Spacer(1, 20))
    
    # Summary info
    story.append(Paragraph(f"Generated on: {datetime.now().strftime('%B %d, %Y at %H:%M')}", styles['Normal']))
    story.append(Paragraph(f"Total Speakers: {speakers.count()}", styles['Normal']))
    story.append(Spacer(1, 20))
    
    # Table data
    data = [['Name', 'Title', 'Organization', 'Type', 'Talk Title']]
    for speaker in speakers:
        data.append([
            speaker.name,
            speaker.title[:30] + '...' if len(speaker.title) > 30 else speaker.title,
            speaker.organization[:25] + '...' if len(speaker.organization) > 25 else speaker.organization,
            speaker.get_speaker_type_display(),
            speaker.talk_title[:40] + '...' if speaker.talk_title and len(speaker.talk_title) > 40 else speaker.talk_title or 'TBA'
        ])
    
    table = Table(data)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 10),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('FONTSIZE', (0, 1), (-1, -1), 8),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    
    story.append(table)
    doc.build(story)
    
    buffer.seek(0)
    response = HttpResponse(buffer, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="speakers_list_{datetime.now().strftime("%Y%m%d_%H%M")}.pdf"'
    return response

def export_speakers_csv(speakers):
    """Export speakers to CSV format"""
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="speakers_list_{datetime.now().strftime("%Y%m%d_%H%M")}.csv"'
    
    writer = csv.writer(response)
    writer.writerow([
        'Name', 'Title', 'Organization', 'Country', 'Speaker Type',
        'Talk Title', 'Session Time', 'Email', 'Website', 'LinkedIn',
        'Is Featured', 'Is Published', 'Created Date'
    ])
    
    for speaker in speakers:
        writer.writerow([
            speaker.name, speaker.title, speaker.organization, speaker.country,
            speaker.get_speaker_type_display(), speaker.talk_title, speaker.session_time,
            speaker.email, speaker.website, speaker.linkedin,
            'Yes' if speaker.is_featured else 'No',
            'Yes' if speaker.is_published else 'No',
            speaker.created_at.strftime('%Y-%m-%d %H:%M')
        ])
    
    return response

def export_speakers_json(speakers):
    """Export speakers to JSON format"""
    data = []
    for speaker in speakers:
        data.append({
            'name': speaker.name,
            'title': speaker.title,
            'organization': speaker.organization,
            'country': speaker.country,
            'speaker_type': speaker.get_speaker_type_display(),
            'talk_title': speaker.talk_title,
            'session_time': speaker.session_time,
            'email': speaker.email,
            'website': speaker.website,
            'linkedin': speaker.linkedin,
            'is_featured': speaker.is_featured,
            'is_published': speaker.is_published,
            'created_date': speaker.created_at.isoformat()
        })
    
    response = HttpResponse(json.dumps(data, indent=2), content_type='application/json')
    response['Content-Disposition'] = f'attachment; filename="speakers_list_{datetime.now().strftime("%Y%m%d_%H%M")}.json"'
    return response

def export_committee_excel(committee_members):
    """Export committee members to Excel format"""
    from openpyxl import Workbook
    from openpyxl.styles import Font, Alignment, PatternFill
    
    wb = Workbook()
    ws = wb.active
    ws.title = "Committee Members"
    
    # Header styling
    header_font = Font(bold=True, size=12)
    header_fill = PatternFill(start_color="366092", end_color="366092", fill_type="solid")
    
    # Headers
    headers = [
        'Name', 'Role', 'Hierarchy Level', 'University/Organization', 
        'Department', 'Email', 'Phone', 'Country', 'Bio Summary', 'Created Date'
    ]
    
    for col, header in enumerate(headers, 1):
        cell = ws.cell(row=1, column=col, value=header)
        cell.font = header_font
        cell.fill = header_fill
        cell.alignment = Alignment(horizontal='center')
    
    # Data rows
    for row, member in enumerate(committee_members, 2):
        ws.cell(row=row, column=1, value=member.name)
        ws.cell(row=row, column=2, value=member.get_role_display())
        ws.cell(row=row, column=3, value=member.hierarchy_level)
        ws.cell(row=row, column=4, value=member.university)
        ws.cell(row=row, column=5, value=member.department)
        ws.cell(row=row, column=6, value=member.email)
        ws.cell(row=row, column=7, value=member.phone)
        ws.cell(row=row, column=8, value=member.country)
        ws.cell(row=row, column=9, value=member.bio[:100] + '...' if member.bio and len(member.bio) > 100 else member.bio)
        ws.cell(row=row, column=10, value=member.created_at.strftime('%Y-%m-%d %H:%M'))
    
    # Adjust column widths
    for column in ws.columns:
        max_length = 0
        column_letter = column[0].column_letter
        for cell in column:
            try:
                if len(str(cell.value)) > max_length:
                    max_length = len(str(cell.value))
            except:
                pass
        adjusted_width = min(max_length + 2, 50)
        ws.column_dimensions[column_letter].width = adjusted_width
    
    # Create response
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = f'attachment; filename="committee_members_{datetime.now().strftime("%Y%m%d_%H%M")}.xlsx"'
    
    wb.save(response)
    return response

def export_committee_pdf(committee_members):
    """Export committee members to PDF format"""
    from reportlab.lib.pagesizes import A4
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
    from reportlab.lib import colors
    
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4)
    styles = getSampleStyleSheet()
    story = []
    
    # Title
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Title'],
        fontSize=18,
        textColor=colors.darkblue,
        alignment=1
    )
    story.append(Paragraph(f"Conference Committee Members", title_style))
    story.append(Spacer(1, 20))
    
    # Summary info
    story.append(Paragraph(f"Generated on: {datetime.now().strftime('%B %d, %Y at %H:%M')}", styles['Normal']))
    story.append(Paragraph(f"Total Members: {committee_members.count()}", styles['Normal']))
    story.append(Spacer(1, 20))
    
    # Table data
    data = [['Name', 'Role', 'Level', 'Organization', 'Email']]
    for member in committee_members:
        data.append([
            member.name,
            member.get_role_display(),
            str(member.hierarchy_level),
            member.university[:30] + '...' if len(member.university) > 30 else member.university,
            member.email
        ])
    
    table = Table(data)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 10),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('FONTSIZE', (0, 1), (-1, -1), 8),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    
    story.append(table)
    doc.build(story)
    
    buffer.seek(0)
    response = HttpResponse(buffer, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="committee_members_{datetime.now().strftime("%Y%m%d_%H%M")}.pdf"'
    return response

def export_committee_csv(committee_members):
    """Export committee members to CSV format"""
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="committee_members_{datetime.now().strftime("%Y%m%d_%H%M")}.csv"'
    
    writer = csv.writer(response)
    writer.writerow([
        'Name', 'Role', 'Hierarchy Level', 'University/Organization',
        'Department', 'Email', 'Phone', 'Country', 'Bio', 'Created Date'
    ])
    
    for member in committee_members:
        writer.writerow([
            member.name, member.get_role_display(), member.hierarchy_level,
            member.university, member.department, member.email, member.phone,
            member.country, member.bio, member.created_at.strftime('%Y-%m-%d %H:%M')
        ])
    
    return response

def export_committee_json(committee_members):
    """Export committee members to JSON format"""
    data = []
    for member in committee_members:
        data.append({
            'name': member.name,
            'role': member.get_role_display(),
            'hierarchy_level': member.hierarchy_level,
            'university': member.university,
            'department': member.department,
            'email': member.email,
            'phone': member.phone,
            'country': member.country,
            'bio': member.bio,
            'created_date': member.created_at.isoformat()
        })
    
    response = HttpResponse(json.dumps(data, indent=2), content_type='application/json')
    response['Content-Disposition'] = f'attachment; filename="committee_members_{datetime.now().strftime("%Y%m%d_%H%M")}.json"'
    return response

def export_logs_excel(logs, days):
    """Export activity logs to Excel format"""
    from openpyxl import Workbook
    from openpyxl.styles import Font, Alignment, PatternFill
    
    wb = Workbook()
    ws = wb.active
    ws.title = f"Activity Logs ({days} days)"
    
    # Header styling
    header_font = Font(bold=True, size=12)
    header_fill = PatternFill(start_color="366092", end_color="366092", fill_type="solid")
    
    # Headers
    headers = [
        'Date/Time', 'User', 'Action', 'Object Type', 'Object', 'Change Message'
    ]
    
    for col, header in enumerate(headers, 1):
        cell = ws.cell(row=1, column=col, value=header)
        cell.font = header_font
        cell.fill = header_fill
        cell.alignment = Alignment(horizontal='center')
    
    # Data rows
    for row, log in enumerate(logs, 2):
        ws.cell(row=row, column=1, value=log.action_time.strftime('%Y-%m-%d %H:%M:%S'))
        ws.cell(row=row, column=2, value=log.user.username if log.user else 'System')
        ws.cell(row=row, column=3, value=log.get_action_flag_display())
        ws.cell(row=row, column=4, value=log.content_type.name if log.content_type else 'Unknown')
        ws.cell(row=row, column=5, value=str(log.object_repr)[:50])
        ws.cell(row=row, column=6, value=log.change_message[:100])
    
    # Adjust column widths
    for column in ws.columns:
        max_length = 0
        column_letter = column[0].column_letter
        for cell in column:
            try:
                if len(str(cell.value)) > max_length:
                    max_length = len(str(cell.value))
            except:
                pass
        adjusted_width = min(max_length + 2, 50)
        ws.column_dimensions[column_letter].width = adjusted_width
    
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = f'attachment; filename="activity_logs_{days}days_{datetime.now().strftime("%Y%m%d_%H%M")}.xlsx"'
    
    wb.save(response)
    return response

def export_logs_csv(logs, days):
    """Export activity logs to CSV format"""
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="activity_logs_{days}days_{datetime.now().strftime("%Y%m%d_%H%M")}.csv"'
    
    writer = csv.writer(response)
    writer.writerow(['Date/Time', 'User', 'Action', 'Object Type', 'Object', 'Change Message'])
    
    for log in logs:
        writer.writerow([
            log.action_time.strftime('%Y-%m-%d %H:%M:%S'),
            log.user.username if log.user else 'System',
            log.get_action_flag_display(),
            log.content_type.name if log.content_type else 'Unknown',
            str(log.object_repr),
            log.change_message
        ])
    
    return response

def export_logs_pdf(logs, days):
    """Export activity logs to PDF format"""
    from reportlab.lib.pagesizes import A4
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
    from reportlab.lib import colors
    
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4)
    styles = getSampleStyleSheet()
    story = []
    
    # Title
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Title'],
        fontSize=18,
        textColor=colors.darkblue,
        alignment=1
    )
    story.append(Paragraph(f"Activity Logs (Last {days} days)", title_style))
    story.append(Spacer(1, 20))
    
    # Summary info
    story.append(Paragraph(f"Generated on: {datetime.now().strftime('%B %d, %Y at %H:%M')}", styles['Normal']))
    story.append(Paragraph(f"Total Activities: {logs.count()}", styles['Normal']))
    story.append(Spacer(1, 20))
    
    # Table data (limited for PDF readability)
    data = [['Date/Time', 'User', 'Action', 'Object']]
    for log in logs[:50]:  # Limit to first 50 for PDF
        data.append([
            log.action_time.strftime('%m/%d %H:%M'),
            log.user.username[:15] if log.user else 'System',
            log.get_action_flag_display(),
            str(log.object_repr)[:30] + '...' if len(str(log.object_repr)) > 30 else str(log.object_repr)
        ])
    
    if logs.count() > 50:
        story.append(Paragraph(f"Showing first 50 of {logs.count()} total activities", styles['Italic']))
        story.append(Spacer(1, 10))
    
    table = Table(data)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 10),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('FONTSIZE', (0, 1), (-1, -1), 8),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    
    story.append(table)
    doc.build(story)
    
    buffer.seek(0)
    response = HttpResponse(buffer, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="activity_logs_{days}days_{datetime.now().strftime("%Y%m%d_%H%M")}.pdf"'
    return response

def export_logs_json(logs, days):
    """Export activity logs to JSON format"""
    data = []
    for log in logs:
        data.append({
            'date_time': log.action_time.isoformat(),
            'user': log.user.username if log.user else 'System',
            'action': log.get_action_flag_display(),
            'object_type': log.content_type.name if log.content_type else 'Unknown',
            'object': str(log.object_repr),
            'change_message': log.change_message
        })
    
    response = HttpResponse(json.dumps(data, indent=2), content_type='application/json')
    response['Content-Disposition'] = f'attachment; filename="activity_logs_{days}days_{datetime.now().strftime("%Y%m%d_%H%M")}.json"'
    return response

def export_schedule_excel(schedules):
    """Export schedule to Excel format"""
    from openpyxl import Workbook
    from openpyxl.styles import Font, Alignment, PatternFill
    
    wb = Workbook()
    ws = wb.active
    ws.title = "Conference Schedule"
    
    # Header styling
    header_font = Font(bold=True, size=12)
    header_fill = PatternFill(start_color="366092", end_color="366092", fill_type="solid")
    
    # Headers
    headers = [
        'Date', 'Day', 'Start Time', 'End Time', 'Title', 'Type',
        'Speaker', 'Location', 'Track', 'Session Chair', 'Capacity',
        'Is Featured', 'Is Published', 'Description'
    ]
    
    for col, header in enumerate(headers, 1):
        cell = ws.cell(row=1, column=col, value=header)
        cell.font = header_font
        cell.fill = header_fill
        cell.alignment = Alignment(horizontal='center')
    
    # Data rows
    for row, schedule in enumerate(schedules, 2):
        ws.cell(row=row, column=1, value=schedule.date.strftime('%Y-%m-%d'))
        ws.cell(row=row, column=2, value=schedule.get_day_display())
        ws.cell(row=row, column=3, value=schedule.start_time.strftime('%H:%M'))
        ws.cell(row=row, column=4, value=schedule.end_time.strftime('%H:%M'))
        ws.cell(row=row, column=5, value=schedule.title)
        ws.cell(row=row, column=6, value=schedule.get_schedule_type_display())
        ws.cell(row=row, column=7, value=schedule.speaker)
        ws.cell(row=row, column=8, value=schedule.location)
        ws.cell(row=row, column=9, value=schedule.track)
        ws.cell(row=row, column=10, value=schedule.session_chair)
        ws.cell(row=row, column=11, value=schedule.capacity)
        ws.cell(row=row, column=12, value='Yes' if schedule.is_featured else 'No')
        ws.cell(row=row, column=13, value='Yes' if schedule.is_published else 'No')
        ws.cell(row=row, column=14, value=schedule.description[:100] + '...' if schedule.description and len(schedule.description) > 100 else schedule.description)
    
    # Adjust column widths
    for column in ws.columns:
        max_length = 0
        column_letter = column[0].column_letter
        for cell in column:
            try:
                if len(str(cell.value)) > max_length:
                    max_length = len(str(cell.value))
            except:
                pass
        adjusted_width = min(max_length + 2, 50)
        ws.column_dimensions[column_letter].width = adjusted_width
    
    # Create response
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = f'attachment; filename="conference_schedule_{datetime.now().strftime("%Y%m%d_%H%M")}.xlsx"'
    
    wb.save(response)
    return response

def export_schedule_pdf(schedules):
    """Export schedule to PDF format"""
    from reportlab.lib.pagesizes import A4
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
    from reportlab.lib import colors
    
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4)
    styles = getSampleStyleSheet()
    story = []
    
    # Title
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Title'],
        fontSize=18,
        textColor=colors.darkblue,
        alignment=1
    )
    story.append(Paragraph(f"Conference Schedule", title_style))
    story.append(Spacer(1, 20))
    
    # Summary info
    story.append(Paragraph(f"Generated on: {datetime.now().strftime('%B %d, %Y at %H:%M')}", styles['Normal']))
    story.append(Paragraph(f"Total Sessions: {schedules.count()}", styles['Normal']))
    story.append(Spacer(1, 20))
    
    # Group by day for better organization
    schedule_by_day = {}
    for schedule in schedules:
        day = schedule.get_day_display()
        if day not in schedule_by_day:
            schedule_by_day[day] = []
        schedule_by_day[day].append(schedule)
    
    for day, day_schedules in schedule_by_day.items():
        # Day header
        day_style = ParagraphStyle(
            'DayHeader',
            parent=styles['Heading2'],
            fontSize=14,
            textColor=colors.darkblue,
            spaceAfter=10
        )
        story.append(Paragraph(f"{day} - {day_schedules[0].date.strftime('%B %d, %Y')}", day_style))
        
        # Table data for this day
        data = [['Time', 'Session', 'Speaker', 'Location']]
        for schedule in day_schedules:
            data.append([
                f"{schedule.start_time.strftime('%H:%M')}-{schedule.end_time.strftime('%H:%M')}",
                schedule.title[:40] + '...' if len(schedule.title) > 40 else schedule.title,
                schedule.speaker[:25] + '...' if schedule.speaker and len(schedule.speaker) > 25 else schedule.speaker or 'TBA',
                schedule.location[:20] + '...' if schedule.location and len(schedule.location) > 20 else schedule.location or 'TBA'
            ])
        
        table = Table(data)
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('FONTSIZE', (0, 1), (-1, -1), 8),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        
        story.append(table)
        story.append(Spacer(1, 15))
    
    doc.build(story)
    
    buffer.seek(0)
    response = HttpResponse(buffer, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="conference_schedule_{datetime.now().strftime("%Y%m%d_%H%M")}.pdf"'
    return response

def export_schedule_csv(schedules):
    """Export schedule to CSV format"""
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="conference_schedule_{datetime.now().strftime("%Y%m%d_%H%M")}.csv"'
    
    writer = csv.writer(response)
    writer.writerow([
        'Date', 'Day', 'Start Time', 'End Time', 'Title', 'Type',
        'Speaker', 'Location', 'Track', 'Session Chair', 'Capacity',
        'Is Featured', 'Is Published', 'Description'
    ])
    
    for schedule in schedules:
        writer.writerow([
            schedule.date.strftime('%Y-%m-%d'),
            schedule.get_day_display(),
            schedule.start_time.strftime('%H:%M'),
            schedule.end_time.strftime('%H:%M'),
            schedule.title,
            schedule.get_schedule_type_display(),
            schedule.speaker,
            schedule.location,
            schedule.track,
            schedule.session_chair,
            schedule.capacity,
            'Yes' if schedule.is_featured else 'No',
            'Yes' if schedule.is_published else 'No',
            schedule.description
        ])
    
    return response

def export_schedule_json(schedules):
    """Export schedule to JSON format"""
    data = []
    for schedule in schedules:
        data.append({
            'date': schedule.date.strftime('%Y-%m-%d'),
            'day': schedule.get_day_display(),
            'start_time': schedule.start_time.strftime('%H:%M'),
            'end_time': schedule.end_time.strftime('%H:%M'),
            'title': schedule.title,
            'type': schedule.get_schedule_type_display(),
            'speaker': schedule.speaker,
            'location': schedule.location,
            'track': schedule.track,
            'session_chair': schedule.session_chair,
            'capacity': schedule.capacity,
            'is_featured': schedule.is_featured,
            'is_published': schedule.is_published,
            'description': schedule.description,
            'color': schedule.color,
            'requirements': schedule.requirements,
            'created_date': schedule.created_at.isoformat()
        })
    
    response = HttpResponse(json.dumps(data, indent=2), content_type='application/json')
    response['Content-Disposition'] = f'attachment; filename="conference_schedule_{datetime.now().strftime("%Y%m%d_%H%M")}.json"'
    return response
