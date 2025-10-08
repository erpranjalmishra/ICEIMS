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
    MaintenanceMode, Notice, EmailLog, UniversityInfo, UniversityGallery,
    SponsorsPageSettings
)

def home(request):
    """Home page view with all conference information - Optimized"""
    from django.core.cache import cache
    from .models import HeroSlide, MarqueeText, ConferenceTopic
    
    # Get marquee timestamp for cache versioning
    marquee_obj = MarqueeText.objects.first()
    marquee_version = marquee_obj.updated_at.timestamp() if marquee_obj else 'none'
    
    # Try to get cached data first - cache key includes marquee version for auto-refresh
    cache_key = f'homepage_data_v5_{marquee_version}'
    context = cache.get(cache_key)
    
    if context is None:
        # Get active notices for home page
        current_time = timezone.now()
        notices = Notice.objects.filter(
            is_active=True,
            start_date__lte=current_time
        ).filter(
            Q(end_date__isnull=True) | Q(end_date__gte=current_time)
        ).filter(
            Q(show_on_pages='') | Q(show_on_pages__icontains='home') | Q(show_on_pages__icontains='all')
        ).order_by('-is_urgent', '-created_at')[:5]  # Limit to 5 most recent
        
        # Get timeline items for home page
        from .models import Timeline
        timeline_items = Timeline.objects.filter(
            is_public=True
        ).order_by('date')[:6]  # Show first 6 items
        
        # Get hero slides (new website control feature)
        hero_slides = HeroSlide.objects.filter(is_active=True).order_by('display_order')
        
        # Get marquee text - convert to dict for caching
        marquee_obj = MarqueeText.get_active()
        marquee_text = None
        if marquee_obj:
            marquee_text = {
                'text': marquee_obj.text,
                'background_color': marquee_obj.background_color,
                'text_color': marquee_obj.text_color,
                'animation_speed': marquee_obj.animation_speed,
            }
        
        # Get all data for the homepage with optimized queries
        context = {
            # Notices
            'notices': list(notices),  # Convert to list for caching
            
            # Timeline items
            'timeline_items': list(timeline_items),
            
            # Hero Slides (new)
            'hero_slides': list(hero_slides) if hero_slides.exists() else None,
            
            # Marquee Text (as dictionary for caching)
            'marquee_text': marquee_text,
            
            # Conference Topics
            'conference_topics': list(ConferenceTopic.objects.filter(is_active=True).only(
                'id', 'title', 'description', 'icon_class', 'display_order'
            ).order_by('display_order', 'title')),
            
            # Slider images (fallback if no hero slides)
            'slider_images': list(Slider.objects.filter(is_active=True).only('id', 'title', 'image', 'order')),
            
            # Committee members - only fetch what's needed
            'committee_members': list(CommitteeMember.objects.all().only(
                'id', 'name', 'role', 'organization', 'image', 'hierarchy_level', 'order'
            )),
            
            # Conference tracks - optimized with only()
            'conference_tracks': list(ConferenceTrack.objects.filter(
                is_active=True
            ).only('id', 'title', 'track_type', 'track_number', 'description').order_by('display_order', 'track_number')),
            
            'regular_tracks': list(ConferenceTrack.objects.filter(
                track_type='regular', is_active=True
            ).only('id', 'title', 'track_number', 'description').order_by('display_order', 'track_number')),
            
            'special_tracks': list(ConferenceTrack.objects.filter(
                track_type='special', is_active=True
            ).only('id', 'title', 'track_number', 'description').order_by('display_order', 'track_number')),
            
            # Tourist attractions - limit fields
            'tourist_attractions': list(TouristAttraction.objects.all().only(
                'id', 'name', 'description', 'image', 'order'
            )),
            
            # Important dates
            'important_dates': list(ImportantDate.objects.all().only(
                'id', 'event', 'date', 'description', 'order'
            )),
            
            # Sponsors - only active ones with all fields for tier/description display
            'sponsors': list(Sponsor.objects.filter(is_active=True).only(
                'id', 'name', 'logo', 'website', 'order', 'partnership_type', 
                'sponsorship_tier', 'partner_type', 'description'
            ).order_by('order')),
            
            # University information for About section
            'university_info': UniversityInfo.objects.filter(is_active=True, show_on_homepage=True).first(),
            
            # Featured gallery images for university slider
            'university_gallery': list(UniversityGallery.objects.filter(
                is_active=True, is_featured=True
            ).only('id', 'title', 'description', 'image').order_by('display_order')[:5]),
            
            # Conference settings
            'conference_settings': ConferenceSettings.objects.only(
                'id', 'site_title', 'conference_dates', 'location'
            ).first(),
        }
        
        # Cache for 1 minute (60 seconds) - signals auto-clear on admin changes
        cache.set(cache_key, context, 60)
    
    return render(request, 'home.html', context)

def about(request):
    """About page view"""
    from .models import AboutPage, AboutObjective, UniversityInfo
    
    conference_settings = ConferenceSettings.objects.first()
    about_page = AboutPage.get_settings()
    objectives = AboutObjective.objects.filter(is_active=True).order_by('order', 'id')
    university_info = UniversityInfo.objects.filter(is_active=True).first()
    
    context = {
        'conference_settings': conference_settings,
        'about_page': about_page,
        'objectives': objectives,
        'university_info': university_info,
    }
    return render(request, 'about.html', context)

def tracks(request):
    """Conference tracks page"""
    context = {
        'regular_tracks': ConferenceTrack.objects.filter(track_type='regular', is_active=True).order_by('display_order', 'track_number'),
        'special_tracks': ConferenceTrack.objects.filter(track_type='special', is_active=True).order_by('display_order', 'track_number'),
    }
    return render(request, 'tracks.html', context)

def committee(request):
    """Committee members page"""
    committee_members = CommitteeMember.objects.filter(is_active=True).order_by('hierarchy_level', 'order', 'name')
    return render(request, 'committee.html', {'committee_members': committee_members})

def committee_bio(request, slug):
    """Individual committee member bio page with share options"""
    from django.shortcuts import get_object_or_404
    from django.conf import settings
    
    member = get_object_or_404(CommitteeMember, slug=slug, is_active=True, enable_bio_page=True)
    
    # Increment page views
    member.increment_page_views()
    
    # Build absolute URL for sharing
    absolute_url = request.build_absolute_uri(member.get_absolute_url())
    
    # Meta tags for social sharing
    meta_description = member.bio[:160] if member.bio else f"Learn more about {member.name}, {member.title} at {member.organization}"
    
    context = {
        'member': member,
        'absolute_url': absolute_url,
        'meta_title': f"{member.name} - {member.get_role_display()} | ICEIMS 2026",
        'meta_description': meta_description,
        'page_type': 'committee_bio',
    }
    
    return render(request, 'committee_bio.html', context)

def attractions(request):
    """Tourist attractions page"""
    attractions = TouristAttraction.objects.filter(is_active=True).order_by('order', 'name')
    return render(request, 'attractions.html', {'attractions': attractions})

def attraction_detail(request, slug):
    """Individual attraction detail page"""
    # Map of slug to template file
    attraction_templates = {
        'red-fort': 'blog/attractions/red-fort.html',
        'india-gate': 'blog/attractions/india-gate.html',
        'lotus-temple': 'blog/attractions/lotus-temple.html',
        'qutub-minar': 'blog/attractions/qutub-minar.html',
        'akshardham-temple': 'blog/attractions/akshardham-temple.html',
        'worlds-of-wonder': 'blog/attractions/worlds-of-wonder.html',
        'great-india-place': 'blog/attractions/great-india-place.html',
        'taj-mahal': 'blog/attractions/taj-mahal.html',
        'humayuns-tomb': 'blog/attractions/humayuns-tomb.html',
        'iskcon-temple': 'blog/attractions/iskcon-temple.html',
        'chandni-chowk': 'blog/attractions/chandni-chowk.html',
        'lodhi-gardens': 'blog/attractions/lodhi-gardens.html',
    }
    
    template = attraction_templates.get(slug)
    if template:
        return render(request, template)
    else:
        # If template doesn't exist, return 404
        from django.http import Http404
        raise Http404("Attraction guide not found")

def university(request):
    """Galgotias University dedicated page with gallery"""
    # Get active university info
    university_info = UniversityInfo.objects.filter(is_active=True).first()
    
    # If no university info exists, create default
    if not university_info:
        university_info = UniversityInfo.objects.create(
            name="Galgotias University",
            about_text="The university began operations in the 2011-2012 academic session and welcomed its first batch of students in July 2011. Since then, it has grown exponentially to become one of India's premier educational institutions, nurturing more than 30K+ students from across the globe.",
            full_description="Galgotias University, established in 2011, is a premier educational institution located in Greater Noida, Uttar Pradesh. The university has rapidly emerged as a leading center for higher education in India, offering a wide range of undergraduate, postgraduate, and doctoral programs across various disciplines including Engineering, Management, Law, and Applied Sciences. With state-of-the-art infrastructure, experienced faculty, and a commitment to excellence, Galgotias University provides a holistic educational experience that prepares students for global careers.",
            is_active=True
        )
    
    # Get gallery images - all active ones
    gallery_images = UniversityGallery.objects.filter(is_active=True).order_by('category', 'display_order')
    
    # Get featured images for homepage slider
    featured_images = UniversityGallery.objects.filter(is_active=True, is_featured=True).order_by('display_order')[:5]
    
    # Group images by category for the gallery
    from itertools import groupby
    gallery_by_category = {}
    for category, images in groupby(gallery_images, key=lambda x: x.category):
        gallery_by_category[category] = list(images)
    
    context = {
        'university_info': university_info,
        'gallery_images': gallery_images,
        'featured_images': featured_images,
        'gallery_by_category': gallery_by_category,
        'categories': UniversityGallery.CATEGORY_CHOICES,
    }
    
    return render(request, 'university.html', context)

def sitemap(request):
    """Public sitemap page showing all available pages"""
    from .models import SitemapLink
    
    # Get all active links from database
    sitemap_links = SitemapLink.objects.filter(is_active=True).order_by('display_order', 'name')
    
    # Convert to template format
    all_pages = [
        {
            'name': link.name,
            'url': link.url,
            'icon': link.icon,
            'description': link.description
        }
        for link in sitemap_links
    ]
    
    context = {
        'all_pages': all_pages,
        'total_pages': len(all_pages),
    }
    
    return render(request, 'sitemap.html', context)

@login_required
@user_passes_test(lambda u: u.is_staff)
def admin_sitemap(request):
    """Admin sitemap showing all admin panel pages"""
    from django.urls import reverse
    
    # Get user profile for permission checking
    profile = getattr(request.user, 'profile', None)
    
    # Organize admin pages by category
    admin_structure = {
        'dashboard': [
            {'name': 'Admin Dashboard', 'url': reverse('conference:admin_dashboard'), 'icon': 'fa-tachometer-alt', 'description': 'Main control panel', 'permission': 'can_access_dashboard'},
        ],
        'content_management': [
            {'name': 'Blog Management', 'url': reverse('conference:blog_list'), 'icon': 'fa-blog', 'description': 'Manage blog posts', 'permission': 'can_manage_blog'},
            {'name': 'Create Blog Post', 'url': reverse('conference:blog_create'), 'icon': 'fa-plus-circle', 'description': 'Write new article', 'permission': 'can_manage_blog'},
            {'name': 'Comments', 'url': reverse('conference:comment_list'), 'icon': 'fa-comments', 'description': 'Moderate comments', 'permission': 'can_manage_blog'},
            {'name': 'Categories', 'url': reverse('conference:category_list'), 'icon': 'fa-tags', 'description': 'Manage categories', 'permission': 'can_manage_blog'},
        ],
        'notices_timeline': [
            {'name': 'Notices', 'url': reverse('conference:notice_list'), 'icon': 'fa-bullhorn', 'description': 'Manage announcements', 'permission': 'can_manage_notices'},
            {'name': 'Create Notice', 'url': reverse('conference:notice_create'), 'icon': 'fa-plus', 'description': 'New announcement', 'permission': 'can_manage_notices'},
            {'name': 'Timeline', 'url': reverse('conference:timeline_list'), 'icon': 'fa-calendar', 'description': 'Manage timeline', 'permission': 'can_manage_timeline'},
            {'name': 'Status Updates', 'url': reverse('conference:status_update_list'), 'icon': 'fa-broadcast-tower', 'description': 'Conference updates', 'permission': 'can_manage_content'},
        ],
        'people_management': [
            {'name': 'Speakers', 'url': reverse('conference:speaker_list'), 'icon': 'fa-microphone', 'description': 'Manage speakers', 'permission': 'can_manage_speakers'},
            {'name': 'Committee Members', 'url': reverse('conference:committee_list'), 'icon': 'fa-users', 'description': 'Manage committee', 'permission': 'can_manage_committee'},
        ],
        'schedule_events': [
            {'name': 'Schedule', 'url': reverse('conference:schedule_list'), 'icon': 'fa-calendar-week', 'description': 'Manage schedule', 'permission': 'can_manage_schedule'},
        ],
        'conference_setup': [
            {'name': 'Conference Tracks', 'url': reverse('conference:track_list'), 'icon': 'fa-layer-group', 'description': 'Manage tracks', 'permission': 'can_manage_tracks'},
            {'name': 'Tourist Attractions', 'url': reverse('conference:attraction_list'), 'icon': 'fa-map-marked-alt', 'description': 'Manage attractions', 'permission': 'can_manage_attractions'},
            {'name': 'Sponsors', 'url': reverse('conference:sponsor_list'), 'icon': 'fa-handshake', 'description': 'Manage sponsors', 'permission': 'can_manage_content'},
        ],
        'university': [
            {'name': 'University Information', 'url': '/admin/conference/universityinfo/', 'icon': 'fa-university', 'description': 'Edit university info', 'permission': 'can_manage_content'},
            {'name': 'University Gallery', 'url': '/admin/conference/universitygallery/', 'icon': 'fa-images', 'description': 'Manage gallery', 'permission': 'can_manage_content'},
        ],
        'user_management': [
            {'name': 'User Management', 'url': reverse('conference:user_management'), 'icon': 'fa-users-cog', 'description': 'Manage users', 'permission': 'can_manage_users'},
            {'name': 'Role Management', 'url': reverse('conference:role_management'), 'icon': 'fa-user-shield', 'description': 'Manage roles', 'permission': 'can_manage_users'},
        ],
        'email_system': [
            {'name': 'Send Email', 'url': reverse('conference:send_email'), 'icon': 'fa-paper-plane', 'description': 'Send emails', 'permission': None},
            {'name': 'Email Templates', 'url': reverse('conference:email_template_list'), 'icon': 'fa-envelope-open-text', 'description': 'Manage templates', 'permission': None},
            {'name': 'Email Logs', 'url': reverse('conference:email_log_list'), 'icon': 'fa-list', 'description': 'View email logs', 'permission': None},
            {'name': 'Security Events', 'url': reverse('conference:security_event_list'), 'icon': 'fa-shield-alt', 'description': 'Security logs', 'permission': None},
        ],
        'system': [
            {'name': 'Maintenance Mode', 'url': reverse('conference:maintenance_list'), 'icon': 'fa-tools', 'description': 'Site maintenance', 'permission': 'can_manage_content'},
            {'name': 'Django Admin', 'url': '/admin/', 'icon': 'fa-database', 'description': 'Django admin panel', 'permission': None},
        ],
    }
    
    # Filter pages based on permissions
    filtered_structure = {}
    for category, pages in admin_structure.items():
        accessible_pages = []
        for page in pages:
            # Check if user has permission
            if request.user.is_superuser:
                accessible_pages.append(page)
            elif page['permission'] is None:
                if request.user.is_staff:
                    accessible_pages.append(page)
            elif profile and profile.has_permission(page['permission']):
                accessible_pages.append(page)
        
        if accessible_pages:
            filtered_structure[category] = accessible_pages
    
    context = {
        'admin_structure': filtered_structure,
        'total_pages': sum(len(pages) for pages in filtered_structure.values()),
    }
    
    return render(request, 'admin/sitemap.html', context)

def contact(request):
    """Contact page view"""
    return render(request, 'contact.html')

def guidelines(request):
    """Dynamic Guidelines page with all categories and guidelines"""
    from .models import GuidelineCategory, Guideline
    
    # Get all active categories with published guidelines
    categories = GuidelineCategory.objects.filter(
        is_active=True,
        guidelines__is_published=True
    ).distinct().prefetch_related('guidelines')
    
    # Get featured guidelines
    featured_guidelines = Guideline.objects.filter(
        is_published=True,
        is_featured=True
    ).select_related('category').order_by('-is_important', 'display_order')[:6]
    
    # Get all published guidelines
    all_guidelines = Guideline.objects.filter(
        is_published=True
    ).select_related('category').prefetch_related('checklist_items').order_by(
        'category__display_order', '-is_important', 'display_order'
    )
    
    # Search functionality
    query = request.GET.get('q', '')
    if query:
        all_guidelines = all_guidelines.filter(
            Q(title__icontains=query) |
            Q(short_description__icontains=query) |
            Q(content__icontains=query)
        )
    
    # Category filter
    category_slug = request.GET.get('category', '')
    selected_category = None
    if category_slug:
        selected_category = GuidelineCategory.objects.filter(slug=category_slug).first()
        if selected_category:
            all_guidelines = all_guidelines.filter(category=selected_category)
    
    context = {
        'categories': categories,
        'featured_guidelines': featured_guidelines,
        'guidelines': all_guidelines,
        'query': query,
        'selected_category': selected_category,
        'total_guidelines': all_guidelines.count(),
    }
    return render(request, 'guidelines.html', context)

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

def speaker_bio(request, slug):
    """Individual speaker bio page with share options"""
    from django.shortcuts import get_object_or_404
    from .models import Speaker
    
    speaker = get_object_or_404(Speaker, slug=slug, is_published=True, enable_bio_page=True)
    
    # Increment page views
    speaker.increment_page_views()
    
    # Build absolute URL for sharing
    absolute_url = request.build_absolute_uri(speaker.get_absolute_url())
    
    # Meta tags for social sharing
    meta_description = speaker.bio[:160] if speaker.bio else f"Learn more about {speaker.name}, {speaker.title} at {speaker.organization}"
    
    context = {
        'speaker': speaker,
        'absolute_url': absolute_url,
        'meta_title': f"{speaker.name} - {speaker.get_speaker_type_display()} | ICEIMS 2026",
        'meta_description': meta_description,
        'page_type': 'speaker_bio',
    }
    
    return render(request, 'speaker_bio.html', context)

def registration(request):
    """Registration page view with dynamic form"""
    from .models import RegistrationCategory, RegistrationSettings, RegistrationFeesTable
    from .forms import ConferenceRegistrationForm
    
    settings = RegistrationSettings.get_settings()
    
    # Check if registration is open
    if not settings.registration_open:
        return render(request, 'registration_closed.html', {
            'message': settings.registration_message
        })
    
    if request.method == 'POST':
        form = ConferenceRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            registration = form.save()
            messages.success(
                request,
                f'Registration submitted successfully! Your registration ID is: {registration.registration_id}'
            )
            return redirect('conference:registration_success', reg_id=registration.registration_id)
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = ConferenceRegistrationForm()
    
    # Get categories for pricing table (old method - still kept for compatibility)
    categories = RegistrationCategory.objects.filter(is_active=True).order_by('display_order')
    
    # Get fees table rows (new method - for custom fees table)
    fees_table_rows = RegistrationFeesTable.objects.filter(is_active=True).order_by('display_order')
    
    context = {
        'form': form,
        'categories': categories,
        'fees_table_rows': fees_table_rows,
        'settings': settings,
    }
    
    return render(request, 'registration.html', context)


def registration_success(request, reg_id):
    """Registration success page"""
    from .models import ConferenceRegistration
    
    try:
        registration = ConferenceRegistration.objects.get(registration_id=reg_id)
        context = {
            'registration': registration,
        }
        return render(request, 'registration_success.html', context)
    except ConferenceRegistration.DoesNotExist:
        messages.error(request, 'Registration not found.')
        return redirect('conference:registration')


def downloads(request):
    """Downloads page for resources and documents"""
    from .models import DownloadResource
    
    resources = DownloadResource.objects.filter(is_active=True)
    featured_resources = resources.filter(is_featured=True)
    
    # Group by category
    categories = {}
    for resource in resources:
        category_name = resource.get_category_display()
        if category_name not in categories:
            categories[category_name] = []
        categories[category_name].append(resource)
    
    context = {
        'featured_resources': featured_resources,
        'all_resources': resources,
        'categories': categories,
    }
    return render(request, 'downloads.html', context)


def download_file(request, resource_id):
    """Handle file download"""
    from .models import DownloadResource
    from django.http import FileResponse, Http404
    
    try:
        resource = DownloadResource.objects.get(id=resource_id, is_active=True)
        resource.increment_downloads()
        
        # Serve the file
        response = FileResponse(resource.file.open('rb'), as_attachment=True, filename=resource.file.name.split('/')[-1])
        return response
    except DownloadResource.DoesNotExist:
        raise Http404("Resource not found")


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
    """Dynamic Awards page with all categories and awards"""
    from .models import AwardCategory, Award, PastWinner, AwardGallery
    
    # Get all active categories with awards
    categories = AwardCategory.objects.filter(
        is_active=True
    ).prefetch_related('awards').order_by('display_order')
    
    # Get featured awards
    featured_awards = Award.objects.filter(
        is_featured=True
    ).select_related('category').order_by('-year', 'display_order')[:6]
    
    # Get current year awards
    current_year = 2026
    current_awards = Award.objects.filter(
        year=current_year
    ).select_related('category').prefetch_related('criteria').order_by('display_order')
    
    # Get announced winners
    announced_winners = Award.objects.filter(
        status='announced',
        year=current_year
    ).select_related('category').order_by('display_order')
    
    # Get open nominations
    open_nominations = Award.objects.filter(
        status='open'
    ).select_related('category').order_by('nomination_end')
    
    # Get past winners (from PastWinner model)
    past_winners = PastWinner.objects.filter(
        is_featured=True
    ).order_by('-year', 'display_order')[:10]
    
    # Get gallery images
    gallery_images = AwardGallery.objects.filter(
        is_active=True,
        year=current_year
    ).order_by('display_order', '-uploaded_at')
    
    # Get hero images for banner section
    hero_images = AwardGallery.objects.filter(
        is_active=True,
        show_on_hero=True
    ).order_by('display_order')[:3]
    
    # Group all awards by category
    awards_by_category = {}
    for category in categories:
        category_awards = current_awards.filter(category=category)
        if category_awards.exists():
            awards_by_category[category] = category_awards
    
    context = {
        'categories': categories,
        'featured_awards': featured_awards,
        'current_awards': current_awards,
        'announced_winners': announced_winners,
        'open_nominations': open_nominations,
        'past_winners': past_winners,
        'awards_by_category': awards_by_category,
        'current_year': current_year,
        'total_awards': current_awards.count(),
        'gallery_images': gallery_images,
        'hero_images': hero_images,
    }
    return render(request, 'awards.html', context)

def sponsors(request):
    """Sponsors page view - dynamic sponsors from database grouped by tier/type"""
    # Get only active sponsors
    all_sponsors = Sponsor.objects.filter(is_active=True).order_by('order')
    
    # Group sponsors by sponsorship tiers
    platinum_sponsors = all_sponsors.filter(partnership_type='sponsorship', sponsorship_tier='platinum')
    gold_sponsors = all_sponsors.filter(partnership_type='sponsorship', sponsorship_tier='gold')
    silver_sponsors = all_sponsors.filter(partnership_type='sponsorship', sponsorship_tier='silver')
    bronze_sponsors = all_sponsors.filter(partnership_type='sponsorship', sponsorship_tier='bronze')
    
    # Group by partner types
    academic_partners = all_sponsors.filter(partnership_type='partnership', partner_type='academic')
    technology_partners = all_sponsors.filter(partnership_type='partnership', partner_type='technology')
    media_partners = all_sponsors.filter(partnership_type='partnership', partner_type='media')
    industry_partners = all_sponsors.filter(partnership_type='partnership', partner_type='industry')
    institutional_partners = all_sponsors.filter(partnership_type='partnership', partner_type='institutional')
    
    conference_settings = ConferenceSettings.objects.first()
    sponsors_page_settings = SponsorsPageSettings.get_settings()
    
    context = {
        'sponsors': all_sponsors,
        'all_sponsors': all_sponsors,
        'platinum_sponsors': platinum_sponsors,
        'gold_sponsors': gold_sponsors,
        'silver_sponsors': silver_sponsors,
        'bronze_sponsors': bronze_sponsors,
        'academic_partners': academic_partners,
        'technology_partners': technology_partners,
        'media_partners': media_partners,
        'industry_partners': industry_partners,
        'institutional_partners': institutional_partners,
        'conference_settings': conference_settings,
        'sponsors_page_settings': sponsors_page_settings,
    }
    return render(request, 'sponsors.html', context)

def animations_test(request):
    """Hidden animations test page - not linked in navigation"""
    return render(request, 'animations-test.html')

# Blog Helper Functions

def is_admin_or_staff(user):
    return user.is_authenticated and (user.is_staff or user.is_superuser)

def has_blog_permission(user):
    """Check if user can manage blog"""
    if not user.is_authenticated:
        return False
    if user.is_superuser:
        return True
    if hasattr(user, 'profile') and user.profile:
        return user.profile.has_permission('can_manage_blog')
    return False

def has_notice_permission(user):
    """Check if user can manage notices"""
    if not user.is_authenticated:
        return False
    if user.is_superuser:
        return True
    if hasattr(user, 'profile') and user.profile:
        return user.profile.has_permission('can_manage_notices')
    return False

def has_timeline_permission(user):
    """Check if user can manage timeline"""
    if not user.is_authenticated:
        return False
    if user.is_superuser:
        return True
    if hasattr(user, 'profile') and user.profile:
        return user.profile.has_permission('can_manage_timeline')
    return False

def has_schedule_permission(user):
    """Check if user can manage schedule"""
    if not user.is_authenticated:
        return False
    if user.is_superuser:
        return True
    if hasattr(user, 'profile') and user.profile:
        return user.profile.has_permission('can_manage_schedule')
    return False

def has_speaker_permission(user):
    """Check if user can manage speakers"""
    if not user.is_authenticated:
        return False
    if user.is_superuser:
        return True
    if hasattr(user, 'profile') and user.profile:
        return user.profile.has_permission('can_manage_speakers')
    return False

def has_committee_permission(user):
    """Check if user can manage committee"""
    if not user.is_authenticated:
        return False
    if user.is_superuser:
        return True
    if hasattr(user, 'profile') and user.profile:
        return user.profile.has_permission('can_manage_committee')
    return False

def has_content_permission(user):
    """Check if user can manage general content (tracks, attractions, etc)"""
    if not user.is_authenticated:
        return False
    if user.is_superuser:
        return True
    if hasattr(user, 'profile') and user.profile:
        return user.profile.has_permission('can_manage_content')
    return False

def has_track_permission(user):
    """Check if user can manage conference tracks"""
    if not user.is_authenticated:
        return False
    if user.is_superuser:
        return True
    if hasattr(user, 'profile') and user.profile:
        return user.profile.has_permission('can_manage_tracks') or user.profile.has_permission('can_manage_content')
    return False

def has_attraction_permission(user):
    """Check if user can manage tourist attractions"""
    if not user.is_authenticated:
        return False
    if user.is_superuser:
        return True
    if hasattr(user, 'profile') and user.profile:
        return user.profile.has_permission('can_manage_attractions') or user.profile.has_permission('can_manage_content')
    return False

def has_export_permission(user):
    """Check if user can export data"""
    if not user.is_authenticated:
        return False
    if user.is_superuser:
        return True
    if hasattr(user, 'profile') and user.profile:
        return user.profile.has_permission('can_export_data')
    return False

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
@user_passes_test(has_blog_permission)
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
@user_passes_test(has_blog_permission)
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
@user_passes_test(has_blog_permission)
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
@user_passes_test(has_blog_permission)
def category_list(request):
    categories = Category.objects.annotate(post_count=Count('posts')).order_by('name')
    
    context = {
        'categories': categories,
    }
    
    return render(request, 'blog/category_list.html', context)

@login_required
@user_passes_test(has_blog_permission)
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
@user_passes_test(has_blog_permission)
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
@user_passes_test(has_blog_permission)
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
@user_passes_test(has_content_permission)
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
@user_passes_test(has_content_permission)
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
@user_passes_test(has_content_permission)
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
@user_passes_test(has_notice_permission)
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
@user_passes_test(has_notice_permission)
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
        link_url = request.POST.get('link_url', '')
        link_text = request.POST.get('link_text', 'Read More')
        
        notice = Notice.objects.create(
            title=title,
            content=content,
            notice_type=notice_type,
            is_active=is_active,
            is_urgent=is_urgent,
            start_date=start_date if start_date else timezone.now(),
            end_date=end_date if end_date else None,
            show_on_pages=show_on_pages,
            link_url=link_url,
            link_text=link_text if link_text else 'Read More',
            created_by=request.user
        )
        
        messages.success(request, f'Notice "{title}" created successfully!')
        return redirect('conference:notice_list')
    
    return render(request, 'admin/notice_create.html')

@ensure_csrf_cookie
@login_required
@user_passes_test(has_notice_permission)
def notice_edit(request, pk):
    """Edit existing notice"""
    notice = get_object_or_404(Notice, pk=pk)
    
    if request.method == 'POST':
        notice.title = request.POST.get('title')
        notice.content = request.POST.get('content')
        notice.notice_type = request.POST.get('notice_type')
        notice.is_active = request.POST.get('is_active') == 'on'
        notice.is_urgent = request.POST.get('is_urgent') == 'on'
        notice.start_date = request.POST.get('start_date') or timezone.now()
        notice.end_date = request.POST.get('end_date') or None
        notice.show_on_pages = request.POST.get('show_on_pages', '')
        notice.link_url = request.POST.get('link_url', '')
        notice.link_text = request.POST.get('link_text', 'Read More')
        
        notice.save()
        
        messages.success(request, f'Notice "{notice.title}" updated successfully!')
        return redirect('conference:notice_list')
    
    context = {
        'notice': notice,
    }
    return render(request, 'admin/notice_edit.html', context)

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
    from .models import (BlogPost, Comment, Notice, MaintenanceMode, Timeline, StatusUpdate, Speaker, CommitteeMember, 
                        Schedule, UserProfile, FAQCategory, FAQ, AIConversation, GuidelineCategory, Guideline, 
                        AwardCategory, Award, PastWinner, SiteSettings, HeroSlide, SliderSettings,
                        VisitorCounter, PageVisitLog)
    
    # Get or create user profile
    profile, created = UserProfile.objects.get_or_create(user=request.user)
    
    # Get statistics
    from .models import ConferenceTrack, TouristAttraction
    
    stats = {
        'blog_posts': BlogPost.objects.count(),
        'published_posts': BlogPost.objects.filter(status='published').count(),
        'pending_comments': Comment.objects.filter(status='pending').count(),
        'active_notices': Notice.objects.filter(is_active=True).count(),
        'maintenance_modes': MaintenanceMode.objects.filter(is_active=True).count(),
        'speakers': Speaker.objects.count(),
        'keynote_speakers': Speaker.objects.filter(speaker_type='keynote').count(),
        'committee_members': CommitteeMember.objects.count(),
        'timeline_items': Timeline.objects.count(),
        'status_updates': StatusUpdate.objects.count(),
        'schedule_items': Schedule.objects.count(),
        'conference_tracks': ConferenceTrack.objects.count(),
        'active_tracks': ConferenceTrack.objects.filter(is_active=True).count(),
        'tourist_attractions': TouristAttraction.objects.count(),
        'active_attractions': TouristAttraction.objects.filter(is_active=True).count(),
        'sponsors': Sponsor.objects.count(),
        'university_info': UniversityInfo.objects.count(),
        'gallery_images': UniversityGallery.objects.count(),
        'faq_categories': FAQCategory.objects.filter(is_active=True).count(),
        'published_faqs': FAQ.objects.filter(is_published=True).count(),
        'total_faqs': FAQ.objects.count(),
        'ai_conversations': AIConversation.objects.count(),
        'guideline_categories': GuidelineCategory.objects.filter(is_active=True).count(),
        'published_guidelines': Guideline.objects.filter(is_published=True).count(),
        'total_guidelines': Guideline.objects.count(),
        'award_categories': AwardCategory.objects.filter(is_active=True).count(),
        'total_awards': Award.objects.count(),
        'announced_awards': Award.objects.filter(status='announced').count(),
        'open_nominations': Award.objects.filter(status='open').count(),
        'past_winners': PastWinner.objects.count(),
        'total_users': User.objects.count(),
        'admin_users': User.objects.filter(is_staff=True).count(),
        'site_settings_configured': SiteSettings.objects.exists(),
        'hero_slides': HeroSlide.objects.count(),
        'active_slides': HeroSlide.objects.filter(is_active=True).count(),
        'slider_settings_configured': SliderSettings.objects.exists(),
        # Visitor Statistics
        'total_visitors': VisitorCounter.get_total_visitors(),
        'today_visitors': VisitorCounter.get_today_visitors(),
        'total_page_visits': PageVisitLog.get_total_visits(),
        'today_page_visits': PageVisitLog.get_today_visits(),
        'unique_visitors_today': PageVisitLog.get_unique_visitors_today(),
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
    
    # Get popular pages
    popular_pages = PageVisitLog.get_popular_pages(limit=10, days=7)
    
    # Get recent visitors (last 10)
    recent_visitors = PageVisitLog.objects.select_related().order_by('-timestamp')[:10]
    
    context = {
        'stats': stats,
        'recent_activities': recent_activities,
        'popular_pages': popular_pages,
        'recent_visitors': recent_visitors,
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
        profile.phone = request.POST.get('phone', '')
        profile.department = request.POST.get('department', '')
        profile.position = request.POST.get('position', '')
        profile.bio = request.POST.get('bio', '')
        
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
@user_passes_test(lambda u: u.is_superuser)
def fix_user_staff_status(request):
    """Fix staff status for admin users who can't login to Django admin"""
    from django.contrib.auth.models import User
    
    if request.method == 'POST':
        # Get all users with admin profile but without staff status
        admin_users = User.objects.filter(profile__is_admin_user=True, is_staff=False)
        
        updated_count = 0
        for user in admin_users:
            user.is_staff = True
            user.save()
            updated_count += 1
        
        if updated_count > 0:
            messages.success(request, f'Successfully granted staff status to {updated_count} admin user(s). They can now login to Django admin panel.')
        else:
            messages.info(request, 'All admin users already have staff status.')
        
        return redirect('conference:user_management')
    
    # GET request - show confirmation page
    admin_users_without_staff = User.objects.filter(profile__is_admin_user=True, is_staff=False)
    
    context = {
        'users_to_fix': admin_users_without_staff,
    }
    return render(request, 'admin/fix_staff_status.html', context)

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
@user_passes_test(has_timeline_permission)
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
@user_passes_test(has_timeline_permission)
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
@user_passes_test(has_timeline_permission)
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
@user_passes_test(has_timeline_permission)
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
@user_passes_test(has_timeline_permission)
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
@user_passes_test(has_timeline_permission)
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
@user_passes_test(has_schedule_permission)
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
@user_passes_test(has_schedule_permission)
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
@user_passes_test(has_schedule_permission)
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
@user_passes_test(has_speaker_permission)
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
@user_passes_test(has_speaker_permission)
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
@user_passes_test(has_speaker_permission)
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
@user_passes_test(has_committee_permission)
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
@user_passes_test(has_committee_permission)
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
    
    from .models import HierarchyLevel
    
    # Get dynamic hierarchy levels from database
    hierarchy_choices = [(level.level_number, f"Level {level.level_number} - {level.level_name}") 
                        for level in HierarchyLevel.objects.filter(is_active=True).order_by('level_number')]
    
    context = {
        'next_order': CommitteeMember.objects.count() + 1,
        'role_choices': CommitteeMember.ROLE_CHOICES,
        'hierarchy_choices': hierarchy_choices,
    }
    return render(request, 'admin/committee_create.html', context)

@login_required
@user_passes_test(has_committee_permission)
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
    
    from .models import HierarchyLevel
    
    # Get dynamic hierarchy levels from database
    hierarchy_choices = [(level.level_number, f"Level {level.level_number} - {level.level_name}") 
                        for level in HierarchyLevel.objects.filter(is_active=True).order_by('level_number')]
    
    context = {
        'committee_member': committee_member,
        'role_choices': CommitteeMember.ROLE_CHOICES,
        'hierarchy_choices': hierarchy_choices,
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
@login_required
@user_passes_test(has_export_permission)
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
@user_passes_test(has_export_permission)
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
@user_passes_test(has_export_permission)
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
@user_passes_test(has_export_permission)
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


# ==================== TRACK MANAGEMENT VIEWS ====================

@login_required
@user_passes_test(has_track_permission)
def track_list(request):
    """List all conference tracks with management options"""
    tracks = ConferenceTrack.objects.all().order_by('display_order', 'track_number')
    
    # Get statistics
    total_tracks = tracks.count()
    active_tracks = tracks.filter(is_active=True).count()
    regular_tracks = tracks.filter(track_type='regular').count()
    special_tracks = tracks.filter(track_type='special').count()
    
    context = {
        'tracks': tracks,
        'total_tracks': total_tracks,
        'active_tracks': active_tracks,
        'regular_tracks': regular_tracks,
        'special_tracks': special_tracks,
    }
    return render(request, 'admin/track_list.html', context)


@login_required
@user_passes_test(has_track_permission)
def track_create(request):
    """Create a new conference track"""
    if request.method == 'POST':
        track_number = request.POST.get('track_number')
        title = request.POST.get('title')
        description = request.POST.get('description', '')
        track_type = request.POST.get('track_type', 'regular')
        track_chair = request.POST.get('track_chair', '')
        is_active = request.POST.get('is_active') == 'on'
        display_order = request.POST.get('display_order', 0)
        color = request.POST.get('color', '#a0352f')
        
        # Handle image upload
        image = request.FILES.get('image')
        
        try:
            track = ConferenceTrack.objects.create(
                track_number=track_number,
                title=title,
                description=description,
                track_type=track_type,
                track_chair=track_chair,
                is_active=is_active,
                display_order=display_order or track_number,
                color=color,
                image=image
            )
            messages.success(request, f'Track "{track.title}" created successfully!')
            return redirect('conference:track_list')
        except Exception as e:
            messages.error(request, f'Error creating track: {str(e)}')
    
    # Get the next available track number
    last_track = ConferenceTrack.objects.all().order_by('-track_number').first()
    next_track_number = (last_track.track_number + 1) if last_track else 1
    
    context = {
        'next_track_number': next_track_number,
    }
    return render(request, 'admin/track_form.html', context)


@login_required
@user_passes_test(has_track_permission)
def track_edit(request, pk):
    """Edit an existing conference track"""
    track = get_object_or_404(ConferenceTrack, pk=pk)
    
    if request.method == 'POST':
        track.track_number = request.POST.get('track_number')
        track.title = request.POST.get('title')
        track.description = request.POST.get('description', '')
        track.track_type = request.POST.get('track_type', 'regular')
        track.track_chair = request.POST.get('track_chair', '')
        track.is_active = request.POST.get('is_active') == 'on'
        track.display_order = request.POST.get('display_order', track.track_number)
        track.color = request.POST.get('color', '#a0352f')
        
        # Handle image upload
        if 'image' in request.FILES:
            track.image = request.FILES['image']
        
        # Handle image removal
        if request.POST.get('remove_image') == 'on' and track.image:
            track.image.delete()
            track.image = None
        
        try:
            track.save()
            messages.success(request, f'Track "{track.title}" updated successfully!')
            return redirect('conference:track_list')
        except Exception as e:
            messages.error(request, f'Error updating track: {str(e)}')
    
    context = {
        'track': track,
        'is_edit': True,
    }
    return render(request, 'admin/track_form.html', context)


@login_required
@user_passes_test(has_track_permission)
def track_delete(request, pk):
    """Delete a conference track"""
    track = get_object_or_404(ConferenceTrack, pk=pk)
    
    if request.method == 'POST':
        track_title = track.title
        track.delete()
        messages.success(request, f'Track "{track_title}" deleted successfully!')
        return redirect('conference:track_list')
    
    context = {
        'track': track,
    }
    return render(request, 'admin/track_confirm_delete.html', context)


@login_required
@user_passes_test(lambda u: u.is_staff or u.is_superuser)
def track_toggle(request, pk):
    """Toggle track active status"""
    track = get_object_or_404(ConferenceTrack, pk=pk)
    track.is_active = not track.is_active
    track.save()
    
    status = "activated" if track.is_active else "deactivated"
    messages.success(request, f'Track "{track.title}" {status} successfully!')
    
    return redirect('conference:track_list')


@login_required
@user_passes_test(has_track_permission)
@require_POST
def track_bulk_action(request):
    """Handle bulk actions on tracks"""
    action = request.POST.get('action')
    track_ids = request.POST.getlist('track_ids')
    
    if not track_ids:
        messages.warning(request, 'No tracks selected.')
        return redirect('conference:track_list')
    
    tracks = ConferenceTrack.objects.filter(id__in=track_ids)
    
    if action == 'activate':
        tracks.update(is_active=True)
        messages.success(request, f'{tracks.count()} track(s) activated successfully!')
    elif action == 'deactivate':
        tracks.update(is_active=False)
        messages.success(request, f'{tracks.count()} track(s) deactivated successfully!')
    elif action == 'delete':
        count = tracks.count()
        tracks.delete()
        messages.success(request, f'{count} track(s) deleted successfully!')
    elif action == 'regular':
        tracks.update(track_type='regular')
        messages.success(request, f'{tracks.count()} track(s) changed to Regular Track!')
    elif action == 'special':
        tracks.update(track_type='special')
        messages.success(request, f'{tracks.count()} track(s) changed to Special Session!')
    else:
        messages.error(request, 'Invalid action selected.')
    
    return redirect('conference:track_list')


# Tourist Attraction Management Views
@login_required
@user_passes_test(has_attraction_permission)
def attraction_list(request):
    """List all tourist attractions"""
    attractions = TouristAttraction.objects.all().order_by('order', 'name')
    
    # Filter by category
    category_filter = request.GET.get('category')
    if category_filter:
        attractions = attractions.filter(category=category_filter)
    
    # Filter by status
    status_filter = request.GET.get('status')
    if status_filter == 'active':
        attractions = attractions.filter(is_active=True)
    elif status_filter == 'inactive':
        attractions = attractions.filter(is_active=False)
    
    # Search functionality
    search = request.GET.get('search')
    if search:
        attractions = attractions.filter(
            Q(name__icontains=search) |
            Q(description__icontains=search) |
            Q(category__icontains=search)
        )
    
    # Statistics
    total_attractions = TouristAttraction.objects.count()
    active_attractions = TouristAttraction.objects.filter(is_active=True).count()
    featured_attractions = TouristAttraction.objects.filter(is_featured=True).count()
    
    context = {
        'attractions': attractions,
        'total_attractions': total_attractions,
        'active_attractions': active_attractions,
        'featured_attractions': featured_attractions,
        'category_filter': category_filter,
        'status_filter': status_filter,
        'search': search,
        'category_choices': TouristAttraction.CATEGORY_CHOICES,
    }
    return render(request, 'admin/attraction_list.html', context)


@login_required
@user_passes_test(has_attraction_permission)
def attraction_create(request):
    """Create new tourist attraction"""
    if request.method == 'POST':
        name = request.POST.get('name')
        slug = request.POST.get('slug') or slugify(name)
        description = request.POST.get('description')
        category = request.POST.get('category')
        image_url = request.POST.get('image_url', '')
        location_url = request.POST.get('location_url', '')
        map_embed = request.POST.get('map_embed', '')
        guide_link = request.POST.get('guide_link', '')
        distance = request.POST.get('distance', '')
        time_required = request.POST.get('time_required', '')
        rating = request.POST.get('rating', 4.5)
        is_featured = request.POST.get('is_featured') == 'on'
        is_active = request.POST.get('is_active') == 'on'
        order = request.POST.get('order', 0)
        
        try:
            attraction = TouristAttraction.objects.create(
                name=name,
                slug=slug,
                description=description,
                category=category,
                image_url=image_url,
                location_url=location_url,
                map_embed=map_embed,
                guide_link=guide_link,
                distance=distance,
                time_required=time_required,
                rating=rating,
                is_featured=is_featured,
                is_active=is_active,
                order=order
            )
            
            # Handle image upload
            if 'image' in request.FILES:
                attraction.image = request.FILES['image']
                attraction.save()
            
            messages.success(request, f'Attraction "{name}" created successfully!')
            return redirect('conference:attraction_list')
        except Exception as e:
            messages.error(request, f'Error creating attraction: {str(e)}')
    
    context = {
        'category_choices': TouristAttraction.CATEGORY_CHOICES,
        'is_edit': False,
    }
    return render(request, 'admin/attraction_form.html', context)


@login_required
@user_passes_test(has_attraction_permission)
def attraction_edit(request, pk):
    """Edit tourist attraction"""
    attraction = get_object_or_404(TouristAttraction, pk=pk)
    
    if request.method == 'POST':
        attraction.name = request.POST.get('name')
        attraction.slug = request.POST.get('slug') or slugify(attraction.name)
        attraction.description = request.POST.get('description')
        attraction.category = request.POST.get('category')
        attraction.image_url = request.POST.get('image_url', '')
        attraction.location_url = request.POST.get('location_url', '')
        attraction.map_embed = request.POST.get('map_embed', '')
        attraction.guide_link = request.POST.get('guide_link', '')
        attraction.distance = request.POST.get('distance', '')
        attraction.time_required = request.POST.get('time_required', '')
        attraction.rating = request.POST.get('rating', 4.5)
        attraction.is_featured = request.POST.get('is_featured') == 'on'
        attraction.is_active = request.POST.get('is_active') == 'on'
        attraction.order = request.POST.get('order', 0)
        
        # Handle image upload
        if 'image' in request.FILES:
            attraction.image = request.FILES['image']
        
        # Handle image removal
        if request.POST.get('remove_image') == 'on' and attraction.image:
            attraction.image.delete()
            attraction.image = None
        
        try:
            attraction.save()
            messages.success(request, f'Attraction "{attraction.name}" updated successfully!')
            return redirect('conference:attraction_list')
        except Exception as e:
            messages.error(request, f'Error updating attraction: {str(e)}')
    
    context = {
        'attraction': attraction,
        'category_choices': TouristAttraction.CATEGORY_CHOICES,
        'is_edit': True,
    }
    return render(request, 'admin/attraction_form.html', context)


@login_required
@user_passes_test(has_attraction_permission)
def attraction_delete(request, pk):
    """Delete tourist attraction"""
    attraction = get_object_or_404(TouristAttraction, pk=pk)
    
    if request.method == 'POST':
        attraction_name = attraction.name
        attraction.delete()
        messages.success(request, f'Attraction "{attraction_name}" deleted successfully!')
        return redirect('conference:attraction_list')
    
    context = {
        'attraction': attraction,
    }
    return render(request, 'admin/attraction_confirm_delete.html', context)


@login_required
@login_required
@user_passes_test(has_attraction_permission)
def attraction_toggle(request, pk):
    """Toggle attraction active status"""
    attraction = get_object_or_404(TouristAttraction, pk=pk)
    attraction.is_active = not attraction.is_active
    attraction.save()
    
    status = "activated" if attraction.is_active else "deactivated"
    messages.success(request, f'Attraction "{attraction.name}" {status} successfully!')
    
    return redirect('conference:attraction_list')


@login_required
@user_passes_test(has_attraction_permission)
@require_POST
def attraction_bulk_action(request):
    """Handle bulk actions on attractions"""
    action = request.POST.get('action')
    attraction_ids = request.POST.getlist('attraction_ids')
    
    if not attraction_ids:
        messages.warning(request, 'No attractions selected.')
        return redirect('conference:attraction_list')
    
    attractions = TouristAttraction.objects.filter(id__in=attraction_ids)
    
    if action == 'activate':
        attractions.update(is_active=True)
        messages.success(request, f'{attractions.count()} attraction(s) activated successfully!')
    elif action == 'deactivate':
        attractions.update(is_active=False)
        messages.success(request, f'{attractions.count()} attraction(s) deactivated successfully!')
    elif action == 'delete':
        count = attractions.count()
        attractions.delete()
        messages.success(request, f'{count} attraction(s) deleted successfully!')
    elif action == 'feature':
        attractions.update(is_featured=True)
        messages.success(request, f'{attractions.count()} attraction(s) marked as featured!')
    elif action == 'unfeature':
        attractions.update(is_featured=False)
        messages.success(request, f'{attractions.count()} attraction(s) unmarked as featured!')
    else:
        messages.error(request, 'Invalid action selected.')
    
    return redirect('conference:attraction_list')


# ============================================================================
# EMAIL MANAGEMENT VIEWS
# ============================================================================

@login_required
@user_passes_test(lambda u: u.is_superuser)
def email_template_list(request):
    """List all email templates"""
    from .models import EmailTemplate
    
    templates = EmailTemplate.objects.all().order_by('template_type', 'name')
    
    # Filter by template type if requested
    template_type = request.GET.get('type')
    if template_type:
        templates = templates.filter(template_type=template_type)
    
    # Search functionality
    search_query = request.GET.get('search')
    if search_query:
        templates = templates.filter(
            Q(name__icontains=search_query) |
            Q(subject__icontains=search_query) |
            Q(body_text__icontains=search_query)
        )
    
    # Pagination
    paginator = Paginator(templates, 20)
    page = request.GET.get('page', 1)
    templates_page = paginator.get_page(page)
    
    context = {
        'templates': templates_page,
        'template_types': EmailTemplate.TEMPLATE_TYPES,
        'current_type': template_type,
        'search_query': search_query,
    }
    return render(request, 'admin/email_template_list.html', context)


@login_required
@user_passes_test(lambda u: u.is_superuser)
def email_template_create(request):
    """Create new email template"""
    from .models import EmailTemplate
    
    if request.method == 'POST':
        template = EmailTemplate(
            name=request.POST.get('name'),
            template_type=request.POST.get('template_type'),
            subject=request.POST.get('subject'),
            body_html=request.POST.get('body_html'),
            body_text=request.POST.get('body_text'),
            template_variables=request.POST.get('template_variables', ''),
            created_by=request.user
        )
        
        try:
            template.save()
            messages.success(request, f'Email template "{template.name}" created successfully!')
            return redirect('conference:email_template_list')
        except Exception as e:
            messages.error(request, f'Error creating template: {str(e)}')
    
    context = {
        'template_types': EmailTemplate.TEMPLATE_TYPES,
    }
    return render(request, 'admin/email_template_form.html', context)


@login_required
@user_passes_test(lambda u: u.is_superuser)
def email_template_edit(request, pk):
    """Edit email template"""
    from .models import EmailTemplate
    
    template = get_object_or_404(EmailTemplate, pk=pk)
    
    if request.method == 'POST':
        template.name = request.POST.get('name')
        template.template_type = request.POST.get('template_type')
        template.subject = request.POST.get('subject')
        template.body_html = request.POST.get('body_html')
        template.body_text = request.POST.get('body_text')
        template.template_variables = request.POST.get('template_variables', '')
        
        try:
            template.save()
            messages.success(request, f'Email template "{template.name}" updated successfully!')
            return redirect('conference:email_template_list')
        except Exception as e:
            messages.error(request, f'Error updating template: {str(e)}')
    
    context = {
        'template': template,
        'template_types': EmailTemplate.TEMPLATE_TYPES,
        'is_edit': True,
    }
    return render(request, 'admin/email_template_form.html', context)


@login_required
@user_passes_test(lambda u: u.is_superuser)
def email_template_delete(request, pk):
    """Delete email template"""
    from .models import EmailTemplate
    
    template = get_object_or_404(EmailTemplate, pk=pk)
    
    if request.method == 'POST':
        template_name = template.name
        template.delete()
        messages.success(request, f'Email template "{template_name}" deleted successfully!')
        return redirect('conference:email_template_list')
    
    context = {
        'template': template,
    }
    return render(request, 'admin/email_template_confirm_delete.html', context)


@login_required
@user_passes_test(lambda u: u.is_superuser)
def email_template_preview(request, pk):
    """Preview email template with sample data"""
    from .models import EmailTemplate
    
    template = get_object_or_404(EmailTemplate, pk=pk)
    
    # Sample context data for preview
    sample_context = {
        'user_name': request.user.get_full_name() or request.user.username,
        'email': request.user.email,
        'username': request.user.username,
        'login_url': request.build_absolute_uri('/admin-panel/login/'),
        'support_email': 'support@iceims2026.com',
        'otp_code': '123456',
        'expiry_minutes': '10',
        'ip_address': request.META.get('REMOTE_ADDR', 'Unknown'),
        'user_agent': request.META.get('HTTP_USER_AGENT', 'Unknown'),
        'login_time': timezone.now().strftime('%Y-%m-%d %H:%M:%S'),
        'location': 'Sample Location',
        'event_type': 'Sample Event',
        'description': 'Sample security event description',
        'time': timezone.now().strftime('%Y-%m-%d %H:%M:%S'),
        'role': 'Administrator',
        'role_name': 'Super Administrator',
        'role_description': 'Full access to all features',
        'purpose': 'Login Verification',
    }
    
    # Replace template variables
    html_content = template.body_html
    for key, value in sample_context.items():
        html_content = html_content.replace(f'{{{{{key}}}}}', str(value))
    
    return HttpResponse(html_content)


@login_required
@user_passes_test(lambda u: u.is_superuser)
def email_log_list(request):
    """List all email logs"""
    from .models import EmailLog
    
    logs = EmailLog.objects.all().select_related('template').order_by('-sent_at')
    
    # Filter by status
    status = request.GET.get('status')
    if status:
        logs = logs.filter(status=status)
    
    # Filter by date range
    date_from = request.GET.get('date_from')
    date_to = request.GET.get('date_to')
    if date_from:
        logs = logs.filter(sent_at__gte=date_from)
    if date_to:
        logs = logs.filter(sent_at__lte=date_to)
    
    # Search by recipient
    search_query = request.GET.get('search')
    if search_query:
        logs = logs.filter(
            Q(recipient_email__icontains=search_query) |
            Q(subject__icontains=search_query)
        )
    
    # Pagination
    paginator = Paginator(logs, 50)
    page = request.GET.get('page', 1)
    logs_page = paginator.get_page(page)
    
    # Statistics
    stats = {
        'total': EmailLog.objects.count(),
        'sent': EmailLog.objects.filter(status='sent').count(),
        'failed': EmailLog.objects.filter(status='failed').count(),
        'pending': EmailLog.objects.filter(status='pending').count(),
    }
    
    context = {
        'logs': logs_page,
        'stats': stats,
        'current_status': status,
        'search_query': search_query,
        'date_from': date_from,
        'date_to': date_to,
    }
    return render(request, 'admin/email_log_list.html', context)


@login_required
@user_passes_test(lambda u: u.is_superuser)
def email_campaign_list(request):
    """List all email campaigns"""
    from .models import EmailCampaign
    
    campaigns = EmailCampaign.objects.all().select_related('template', 'created_by').order_by('-created_at')
    
    # Filter by status
    status = request.GET.get('status')
    if status:
        campaigns = campaigns.filter(status=status)
    
    # Search
    search_query = request.GET.get('search')
    if search_query:
        campaigns = campaigns.filter(
            Q(name__icontains=search_query) |
            Q(description__icontains=search_query)
        )
    
    # Pagination
    paginator = Paginator(campaigns, 20)
    page = request.GET.get('page', 1)
    campaigns_page = paginator.get_page(page)
    
    context = {
        'campaigns': campaigns_page,
        'current_status': status,
        'search_query': search_query,
    }
    return render(request, 'admin/email_campaign_list.html', context)


@login_required
@user_passes_test(lambda u: u.is_superuser)
def email_campaign_create(request):
    """Create new email campaign"""
    from .models import EmailCampaign, EmailTemplate
    from .email_utils import send_bulk_email
    
    if request.method == 'POST':
        campaign = EmailCampaign(
            name=request.POST.get('name'),
            description=request.POST.get('description'),
            template_id=request.POST.get('template_id'),
            recipient_filter=request.POST.get('recipient_filter', 'all'),
            created_by=request.user
        )
        
        # Handle scheduled send
        scheduled_for = request.POST.get('scheduled_for')
        if scheduled_for:
            campaign.scheduled_for = scheduled_for
            campaign.status = 'scheduled'
        else:
            campaign.status = 'draft'
        
        try:
            campaign.save()
            
            # If send immediately is checked
            if request.POST.get('send_immediately') == 'on' and not scheduled_for:
                # Get recipients based on filter
                recipients = []
                if campaign.recipient_filter == 'all':
                    recipients = User.objects.filter(email__isnull=False).values_list('email', flat=True)
                elif campaign.recipient_filter == 'admins':
                    recipients = User.objects.filter(is_staff=True, email__isnull=False).values_list('email', flat=True)
                elif campaign.recipient_filter == 'superusers':
                    recipients = User.objects.filter(is_superuser=True, email__isnull=False).values_list('email', flat=True)
                
                if recipients:
                    # Send emails
                    success_count, fail_count = send_bulk_email(
                        template=campaign.template,
                        recipients=list(recipients),
                        context={},
                        campaign=campaign
                    )
                    
                    campaign.emails_sent = success_count
                    campaign.emails_failed = fail_count
                    campaign.status = 'completed'
                    campaign.sent_at = timezone.now()
                    campaign.save()
                    
                    messages.success(request, f'Campaign "{campaign.name}" sent! {success_count} sent, {fail_count} failed.')
                else:
                    messages.warning(request, f'Campaign "{campaign.name}" created but no recipients found.')
            else:
                messages.success(request, f'Campaign "{campaign.name}" created successfully!')
            
            return redirect('conference:email_campaign_list')
        except Exception as e:
            messages.error(request, f'Error creating campaign: {str(e)}')
    
    templates = EmailTemplate.objects.all()
    
    context = {
        'templates': templates,
    }
    return render(request, 'admin/email_campaign_form.html', context)


@login_required
@user_passes_test(lambda u: u.is_superuser)
def email_campaign_send(request, pk):
    """Send an existing email campaign"""
    from .models import EmailCampaign
    from .email_utils import send_bulk_email
    
    campaign = get_object_or_404(EmailCampaign, pk=pk)
    
    if request.method == 'POST':
        # Get recipients based on filter
        recipients = []
        if campaign.recipient_filter == 'all':
            recipients = User.objects.filter(email__isnull=False).values_list('email', flat=True)
        elif campaign.recipient_filter == 'admins':
            recipients = User.objects.filter(is_staff=True, email__isnull=False).values_list('email', flat=True)
        elif campaign.recipient_filter == 'superusers':
            recipients = User.objects.filter(is_superuser=True, email__isnull=False).values_list('email', flat=True)
        
        if recipients:
            # Send emails
            success_count, fail_count = send_bulk_email(
                template=campaign.template,
                recipients=list(recipients),
                context={},
                campaign=campaign
            )
            
            campaign.emails_sent = success_count
            campaign.emails_failed = fail_count
            campaign.status = 'completed'
            campaign.sent_at = timezone.now()
            campaign.save()
            
            messages.success(request, f'Campaign sent! {success_count} emails sent, {fail_count} failed.')
        else:
            messages.warning(request, 'No recipients found for this campaign.')
        
        return redirect('conference:email_campaign_list')
    
    # Count recipients for confirmation
    recipient_count = 0
    if campaign.recipient_filter == 'all':
        recipient_count = User.objects.filter(email__isnull=False).count()
    elif campaign.recipient_filter == 'admins':
        recipient_count = User.objects.filter(is_staff=True, email__isnull=False).count()
    elif campaign.recipient_filter == 'superusers':
        recipient_count = User.objects.filter(is_superuser=True, email__isnull=False).count()
    
    context = {
        'campaign': campaign,
        'recipient_count': recipient_count,
    }
    return render(request, 'admin/email_campaign_confirm_send.html', context)


@login_required
@user_passes_test(lambda u: u.is_superuser)
def security_event_list(request):
    """List all security events"""
    from .models import SecurityEvent
    
    events = SecurityEvent.objects.all().select_related('user').order_by('-created_at')
    
    # Filter by event type
    event_type = request.GET.get('type')
    if event_type:
        events = events.filter(event_type=event_type)
    
    # Filter by user
    user_id = request.GET.get('user')
    if user_id:
        events = events.filter(user_id=user_id)
    
    # Filter by date range
    date_from = request.GET.get('date_from')
    date_to = request.GET.get('date_to')
    if date_from:
        events = events.filter(created_at__gte=date_from)
    if date_to:
        events = events.filter(created_at__lte=date_to)
    
    # Pagination
    paginator = Paginator(events, 50)
    page = request.GET.get('page', 1)
    events_page = paginator.get_page(page)
    
    # Get users for filter dropdown
    users = User.objects.filter(id__in=SecurityEvent.objects.values_list('user_id', flat=True).distinct())
    
    context = {
        'events': events_page,
        'event_types': SecurityEvent.EVENT_TYPES,
        'users': users,
        'current_type': event_type,
        'current_user': user_id,
        'date_from': date_from,
        'date_to': date_to,
    }
    return render(request, 'admin/security_event_list.html', context)


@login_required
@user_passes_test(lambda u: u.is_superuser)
def send_email(request):
    """Send email directly from admin panel"""
    from .models import EmailTemplate, ScheduledEmail
    from .email_utils import send_bulk_email
    from django.contrib.auth.models import User
    
    templates = EmailTemplate.objects.filter(is_active=True)
    
    # Calculate stats
    stats = {
        'total_users': User.objects.count(),
        'staff_count': User.objects.filter(is_staff=True).count(),
        'emails_today': EmailLog.objects.filter(
            created_at__date=timezone.now().date()
        ).count(),
        'scheduled_count': ScheduledEmail.objects.filter(status='pending').count(),
    }
    
    if request.method == 'POST':
        template_id = request.POST.get('template')
        recipient_type = request.POST.get('recipient_type')
        send_type = request.POST.get('send_type')
        
        try:
            template = EmailTemplate.objects.get(id=template_id)
            
            # Get recipients based on type
            recipients = []
            recipient_count = 0
            
            if recipient_type == 'all_users':
                recipients = list(User.objects.filter(email__isnull=False).exclude(email='').values_list('email', flat=True))
            elif recipient_type == 'all_staff':
                recipients = list(User.objects.filter(is_staff=True, email__isnull=False).exclude(email='').values_list('email', flat=True))
            elif recipient_type == 'all_reviewers':
                recipients = list(User.objects.filter(groups__name='Reviewers', email__isnull=False).exclude(email='').values_list('email', flat=True))
            elif recipient_type == 'all_authors':
                recipients = list(User.objects.filter(groups__name='Authors', email__isnull=False).exclude(email='').values_list('email', flat=True))
            elif recipient_type == 'specific':
                specific_emails = request.POST.get('specific_emails', '')
                recipients = [email.strip() for email in specific_emails.split(',') if email.strip()]
            
            if not recipients:
                messages.warning(request, 'No recipients found for the selected type.')
                return redirect('conference:send_email')
            
            recipient_count = len(recipients)
            
            if send_type == 'scheduled':
                # Create scheduled email
                scheduled_time = request.POST.get('scheduled_time')
                if not scheduled_time:
                    messages.error(request, 'Please provide a scheduled time.')
                    return redirect('conference:send_email')
                
                scheduled_email = ScheduledEmail.objects.create(
                    template=template,
                    recipient_type=recipient_type,
                    recipient_emails=','.join(recipients) if recipient_type == 'specific' else '',
                    recipient_count=recipient_count,
                    scheduled_time=scheduled_time,
                    created_by=request.user
                )
                
                messages.success(request, f'✓ Email scheduled successfully for {scheduled_time}. {recipient_count} recipients will receive this email.')
                return redirect('conference:scheduled_emails')
            else:
                # Send immediately - render template with context
                context = {
                    'conference_name': 'ICEIMS 2026',
                    'site_url': request.build_absolute_uri('/'),
                    'year': timezone.now().year,
                }
                
                # Render subject and body
                subject = template.subject
                for key, value in context.items():
                    subject = subject.replace(f'{{{{{key}}}}}', str(value))
                
                html_message = template.body_html
                for key, value in context.items():
                    html_message = html_message.replace(f'{{{{{key}}}}}', str(value))
                
                text_message = template.body_text or html_message
                
                # Send emails using correct function signature
                email_logs = send_bulk_email(
                    subject=subject,
                    message=text_message,
                    recipient_list=recipients,
                    html_message=html_message
                )
                
                # Count results
                success_count = sum(1 for log in email_logs if log.status == 'sent')
                fail_count = len(email_logs) - success_count
                
                if fail_count == 0:
                    messages.success(request, f'✓ Email sent successfully to {success_count} recipients!')
                else:
                    messages.warning(request, f'Email sent to {success_count} recipients. {fail_count} failed.')
                
                return redirect('conference:email_log_list')
                
        except EmailTemplate.DoesNotExist:
            messages.error(request, 'Template not found. Please select a valid template.')
        except Exception as e:
            messages.error(request, f'Error sending email: {str(e)}')
    
    context = {
        'templates': templates,
        'stats': stats,
    }
    return render(request, 'admin/send_email.html', context)


@login_required
@user_passes_test(lambda u: u.is_superuser)
def scheduled_emails(request):
    """List all scheduled emails"""
    from .models import ScheduledEmail
    
    emails = ScheduledEmail.objects.all().select_related('template', 'created_by').order_by('scheduled_time')
    
    # Filter by status
    status = request.GET.get('status')
    if status:
        emails = emails.filter(status=status)
    
    # Filter by date range
    date_from = request.GET.get('date_from')
    date_to = request.GET.get('date_to')
    if date_from:
        emails = emails.filter(scheduled_time__gte=date_from)
    if date_to:
        emails = emails.filter(scheduled_time__lte=date_to)
    
    # Pagination
    paginator = Paginator(emails, 20)
    page = request.GET.get('page', 1)
    emails_page = paginator.get_page(page)
    
    context = {
        'scheduled_emails': emails_page,
    }
    return render(request, 'admin/scheduled_emails.html', context)


@login_required
@user_passes_test(lambda u: u.is_superuser)
def send_scheduled_email_now(request, pk):
    """Send a scheduled email immediately"""
    from .models import ScheduledEmail
    from .email_utils import send_bulk_email
    
    scheduled_email = get_object_or_404(ScheduledEmail, pk=pk)
    
    if scheduled_email.status != 'pending':
        messages.warning(request, 'This email has already been processed.')
        return redirect('conference:scheduled_emails')
    
    try:
        # Get recipients
        recipients = []
        if scheduled_email.recipient_type == 'specific':
            recipients = [email.strip() for email in scheduled_email.recipient_emails.split(',') if email.strip()]
        elif scheduled_email.recipient_type == 'all_users':
            recipients = list(User.objects.filter(email__isnull=False).values_list('email', flat=True))
        elif scheduled_email.recipient_type == 'all_staff':
            recipients = list(User.objects.filter(is_staff=True, email__isnull=False).values_list('email', flat=True))
        
        # Send emails
        success_count, fail_count = send_bulk_email(
            template=scheduled_email.template,
            recipients=recipients,
            context={'conference_name': 'ICEIMS 2026'},
            campaign=None
        )
        
        # Update scheduled email
        scheduled_email.status = 'sent'
        scheduled_email.sent_time = timezone.now()
        scheduled_email.emails_sent = success_count
        scheduled_email.emails_failed = fail_count
        scheduled_email.save()
        
        messages.success(request, f'Email sent! {success_count} successful, {fail_count} failed.')
    except Exception as e:
        scheduled_email.status = 'failed'
        scheduled_email.error_message = str(e)
        scheduled_email.save()
        messages.error(request, f'Error sending email: {str(e)}')
    
    return redirect('conference:scheduled_emails')


@login_required
@user_passes_test(lambda u: u.is_superuser)
def cancel_scheduled_email(request, pk):
    """Cancel a scheduled email"""
    from .models import ScheduledEmail
    
    scheduled_email = get_object_or_404(ScheduledEmail, pk=pk)
    
    if scheduled_email.status != 'pending':
        messages.warning(request, 'This email cannot be cancelled.')
    else:
        scheduled_email.status = 'cancelled'
        scheduled_email.save()
        messages.success(request, 'Scheduled email cancelled successfully.')
    
    return redirect('conference:scheduled_emails')


@login_required
@user_passes_test(lambda u: u.is_superuser)
def email_settings(request):
    """Display email configuration settings"""
    from django.conf import settings
    
    # Check if email is properly configured
    is_configured = (
        settings.EMAIL_HOST_USER != 'your-email@gmail.com' and
        settings.EMAIL_HOST_PASSWORD != 'your-app-password'
    )
    
    context = {
        'email_backend': settings.EMAIL_BACKEND,
        'email_host': settings.EMAIL_HOST,
        'email_port': settings.EMAIL_PORT,
        'email_use_tls': settings.EMAIL_USE_TLS,
        'email_host_user': settings.EMAIL_HOST_USER,
        'is_configured': is_configured,
    }
    
    return render(request, 'admin/email_settings.html', context)


# Sponsor Management Views
@login_required
@user_passes_test(has_content_permission)
def sponsor_list(request):
    """List all sponsors"""
    sponsors_list = Sponsor.objects.all().order_by('order')
    
    context = {
        'sponsors': sponsors_list,
        'total_sponsors': sponsors_list.count(),
    }
    return render(request, 'admin/sponsor_list.html', context)


@login_required
@user_passes_test(has_content_permission)
def sponsor_create(request):
    """Create new sponsor"""
    if request.method == 'POST':
        name = request.POST.get('name')
        website = request.POST.get('website', '')
        partnership_type = request.POST.get('partnership_type', 'sponsorship')
        sponsorship_tier = request.POST.get('sponsorship_tier', '')
        partner_type = request.POST.get('partner_type', '')
        description = request.POST.get('description', '')
        order = request.POST.get('order', 0)
        is_active = request.POST.get('is_active') == 'on'
        
        sponsor = Sponsor.objects.create(
            name=name,
            website=website,
            partnership_type=partnership_type,
            sponsorship_tier=sponsorship_tier,
            partner_type=partner_type,
            description=description,
            order=order,
            is_active=is_active
        )
        
        # Handle logo upload
        if 'logo' in request.FILES:
            sponsor.logo = request.FILES['logo']
            sponsor.save()
        
        messages.success(request, f'Sponsor/Partner "{name}" created successfully!')
        
        # Clear cache to update homepage
        from django.core.cache import cache
        cache.delete('homepage_data_v2')
        
        return redirect('conference:sponsor_list')
    
    return render(request, 'admin/sponsor_create.html')


@login_required
@user_passes_test(has_content_permission)
def sponsor_edit(request, pk):
    """Edit sponsor"""
    sponsor = get_object_or_404(Sponsor, pk=pk)
    
    if request.method == 'POST':
        sponsor.name = request.POST.get('name')
        sponsor.website = request.POST.get('website', '')
        sponsor.partnership_type = request.POST.get('partnership_type', 'sponsorship')
        sponsor.sponsorship_tier = request.POST.get('sponsorship_tier', '')
        sponsor.partner_type = request.POST.get('partner_type', '')
        sponsor.description = request.POST.get('description', '')
        sponsor.order = request.POST.get('order', 0)
        sponsor.is_active = request.POST.get('is_active') == 'on'
        
        # Handle logo upload
        if 'logo' in request.FILES:
            # Delete old logo if exists
            if sponsor.logo:
                try:
                    sponsor.logo.delete()
                except:
                    pass
            sponsor.logo = request.FILES['logo']
        
        sponsor.save()
        messages.success(request, f'Sponsor/Partner "{sponsor.name}" updated successfully!')
        
        # Clear cache to update homepage
        from django.core.cache import cache
        cache.delete('homepage_data_v2')
        
        return redirect('conference:sponsor_list')
    
    context = {
        'sponsor': sponsor,
    }
    return render(request, 'admin/sponsor_edit.html', context)


@login_required
@user_passes_test(is_admin_or_staff)
@require_POST
def sponsor_delete(request, pk):
    """Delete sponsor"""
    sponsor = get_object_or_404(Sponsor, pk=pk)
    name = sponsor.name
    
    # Delete logo file if exists
    if sponsor.logo:
        try:
            sponsor.logo.delete()
        except:
            pass
    
    sponsor.delete()
    messages.success(request, f'Sponsor "{name}" deleted successfully!')
    
    # Clear cache to update homepage
    from django.core.cache import cache
    cache.delete('homepage_data_v2')
    
    return redirect('conference:sponsor_list')


@login_required
@user_passes_test(is_admin_or_staff)
@require_POST
def sponsor_bulk_action(request):
    """Handle bulk actions on sponsors"""
    action = request.POST.get('action')
    selected_ids = request.POST.getlist('selected_sponsors')
    
    if not selected_ids:
        messages.error(request, 'No sponsors selected.')
        return redirect('conference:sponsor_list')
    
    sponsors_qs = Sponsor.objects.filter(id__in=selected_ids)
    count = sponsors_qs.count()
    
    if action == 'delete':
        # Delete logo files
        for sponsor in sponsors_qs:
            if sponsor.logo:
                try:
                    sponsor.logo.delete()
                except:
                    pass
        sponsors_qs.delete()
        messages.success(request, f'{count} sponsor{"s" if count != 1 else ""} deleted successfully.')
    
    # Clear cache to update homepage
    from django.core.cache import cache
    cache.delete('homepage_data_v2')
    
    return redirect('conference:sponsor_list')


# =============================================================================
# FAQ VIEWS WITH AI INTEGRATION
# =============================================================================

def faq_page(request):
    """FAQ page with categories and AI chatbot"""
    from .models import FAQCategory, FAQ
    
    # Get all active categories with published FAQs
    categories = FAQCategory.objects.filter(
        is_active=True,
        faqs__is_published=True
    ).distinct().prefetch_related('faqs')
    
    # Get featured FAQs
    featured_faqs = FAQ.objects.filter(
        is_published=True,
        is_featured=True
    ).select_related('category').order_by('-priority', 'display_order')[:5]
    
    # Get all published FAQs grouped by category
    all_faqs = FAQ.objects.filter(
        is_published=True
    ).select_related('category').order_by('category__display_order', '-priority', 'display_order')
    
    # Search functionality
    query = request.GET.get('q', '')
    if query:
        all_faqs = all_faqs.filter(
            Q(question__icontains=query) |
            Q(answer__icontains=query) |
            Q(tags__icontains=query) |
            Q(keywords__icontains=query)
        )
    
    # Category filter
    category_slug = request.GET.get('category', '')
    selected_category = None
    if category_slug:
        selected_category = FAQCategory.objects.filter(slug=category_slug).first()
        if selected_category:
            all_faqs = all_faqs.filter(category=selected_category)
    
    context = {
        'categories': categories,
        'featured_faqs': featured_faqs,
        'faqs': all_faqs,
        'query': query,
        'selected_category': selected_category,
        'total_faqs': all_faqs.count(),
    }
    
    return render(request, 'faq.html', context)


@require_POST
@csrf_protect
def faq_ask_ai(request):
    """AI-powered FAQ answering using Gemini API"""
    import json
    import time
    import uuid
    from django.conf import settings
    from .models import FAQ, AIConversation
    
    try:
        # Get question from request
        data = json.loads(request.body)
        user_question = data.get('question', '').strip()
        session_id = data.get('session_id', str(uuid.uuid4()))
        
        if not user_question:
            return JsonResponse({'error': 'Please provide a question'}, status=400)
        
        if len(user_question) < 5:
            return JsonResponse({'error': 'Question too short. Please be more specific.'}, status=400)
        
        # Check if Gemini API is configured
        api_key = settings.GEMINI_API_KEY
        if not api_key:
            return JsonResponse({
                'error': 'AI service is not configured. Please contact the administrator.'
            }, status=500)
        
        start_time = time.time()
        
        # Try to find matching FAQ first
        matched_faq = FAQ.objects.filter(
            is_published=True
        ).filter(
            Q(question__icontains=user_question) |
            Q(keywords__icontains=user_question) |
            Q(tags__icontains=user_question)
        ).first()
        
        # If exact match found, return it
        if matched_faq:
            matched_faq.increment_views()
            response_time = time.time() - start_time
            
            # Save conversation
            conversation = AIConversation.objects.create(
                session_id=session_id,
                user_question=user_question,
                ai_response=matched_faq.answer,
                matched_faq=matched_faq,
                response_time=response_time,
                ip_address=get_client_ip(request),
                user_agent=request.META.get('HTTP_USER_AGENT', '')
            )
            
            return JsonResponse({
                'answer': matched_faq.answer,
                'source': 'faq',
                'faq_id': matched_faq.id,
                'category': matched_faq.category.name if matched_faq.category else None,
                'response_time': response_time
            })
        
        # Use Gemini AI to generate answer
        try:
            import google.generativeai as genai
            
            # Configure Gemini
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel(settings.GEMINI_MODEL)
            
            # Get all published FAQs for context
            faq_context = "\n\n".join([
                f"Q: {faq.question}\nA: {faq.answer}"
                for faq in FAQ.objects.filter(is_published=True)[:20]
            ])
            
            # Create prompt
            prompt = f"""You are a helpful assistant for the ICEIMS 2026 (International Conference on Energy and Intelligent Manufacturing Systems). 
Answer the user's question based on the following FAQ database and general conference knowledge.

FAQ Database:
{faq_context}

User Question: {user_question}

Instructions:
1. If the question is directly related to FAQs above, provide the relevant answer.
2. If not found in FAQs, provide a helpful answer based on general conference knowledge.
3. Keep answers concise, professional, and helpful.
4. If you don't know, suggest contacting the conference organizers.
5. Format your answer in clear paragraphs.

Answer:"""
            
            # Generate response
            response = model.generate_content(prompt)
            ai_answer = response.text.strip()
            
            response_time = time.time() - start_time
            
            # Save conversation
            conversation = AIConversation.objects.create(
                session_id=session_id,
                user_question=user_question,
                ai_response=ai_answer,
                matched_faq=None,
                response_time=response_time,
                ip_address=get_client_ip(request),
                user_agent=request.META.get('HTTP_USER_AGENT', '')
            )
            
            return JsonResponse({
                'answer': ai_answer,
                'source': 'ai',
                'response_time': response_time,
                'conversation_id': conversation.id
            })
            
        except Exception as ai_error:
            return JsonResponse({
                'error': f'AI service error: {str(ai_error)}'
            }, status=500)
    
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid request format'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@require_POST
@csrf_protect
def faq_mark_helpful(request, faq_id):
    """Mark FAQ as helpful"""
    from .models import FAQ
    
    try:
        faq = get_object_or_404(FAQ, id=faq_id, is_published=True)
        faq.mark_helpful()
        
        return JsonResponse({
            'success': True,
            'helpful_count': faq.helpful_count,
            'total_votes': faq.helpful_count + faq.not_helpful_count,
            'ratio': faq.helpfulness_ratio
        })
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@require_POST
@csrf_protect
def faq_mark_not_helpful(request, faq_id):
    """Mark FAQ as not helpful"""
    from .models import FAQ
    
    try:
        faq = get_object_or_404(FAQ, id=faq_id, is_published=True)
        faq.mark_not_helpful()
        
        return JsonResponse({
            'success': True,
            'not_helpful_count': faq.not_helpful_count,
            'total_votes': faq.helpful_count + faq.not_helpful_count,
            'ratio': faq.helpfulness_ratio
        })
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@require_POST
@csrf_protect
def faq_conversation_feedback(request, conversation_id):
    """Submit feedback for AI conversation"""
    from .models import AIConversation
    import json
    
    try:
        data = json.loads(request.body)
        conversation = get_object_or_404(AIConversation, id=conversation_id)
        
        conversation.was_helpful = data.get('helpful', None)
        conversation.feedback_text = data.get('feedback', '')
        conversation.save()
        
        return JsonResponse({'success': True})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


def get_client_ip(request):
    """Get client IP address from request"""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def get_visitor_count(request):
    """API endpoint to get real-time visitor count"""
    from .models import VisitorCounter
    from django.core.cache import cache
    
    # Cache the count for 30 seconds to reduce database load
    cache_key = 'visitor_total_count'
    visitor_count = cache.get(cache_key)
    
    if visitor_count is None:
        visitor_count = VisitorCounter.get_total_visitors()
        cache.set(cache_key, visitor_count, 30)  # Cache for 30 seconds
    
    return JsonResponse({
        'total': visitor_count,
        'success': True
    })
