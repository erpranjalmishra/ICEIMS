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
    BlogPost, Category, Tag, Comment, Newsletter
)

def home(request):
    """Home page view with all conference information"""
    
    # Get all data for the homepage
    context = {
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
    committee_members = CommitteeMember.objects.all()
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
    """Keynote speakers page view"""
    return render(request, 'keynotes.html')

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
    """Schedule page view"""
    return render(request, 'schedule.html')

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
        return redirect('conference:home')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            next_url = request.GET.get('next', 'conference:home')
            messages.success(request, f'Welcome back, {user.get_full_name() or user.username}!')
            return redirect(next_url)
        else:
            messages.error(request, 'Invalid username or password.')
    
    return render(request, 'auth/login.html')

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
