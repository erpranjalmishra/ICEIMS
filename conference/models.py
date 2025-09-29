from django.db import models
from django.utils.text import slugify
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone
from PIL import Image
import os

class CommitteeMember(models.Model):
    ROLE_CHOICES = [
        ('chief_patron', 'Chief Patron'),
        ('patron', 'Patron'),
        ('chair', 'Conference Chair'),
        ('co_chair', 'Conference Co-Chair'),
        ('program_chair', 'Program Chair'),
        ('technical_chair', 'Technical Chair'),
        ('organizing_chair', 'Organizing Chair'),
        ('organizing_co_chair', 'Organizing Co-Chair'),
        ('organizing_secretary', 'Organizing Secretary'),
        ('publication_chair', 'Publication Chair'),
        ('registration_chair', 'Registration Chair'),
        ('publicity_chair', 'Publicity Chair'),
        ('finance_chair', 'Finance Chair'),
        ('local_arrangement', 'Local Arrangement'),
        ('member', 'Committee Member'),
    ]
    
    HIERARCHY_LEVELS = [
        (1, 'Level 1 - Chief Patron'),
        (2, 'Level 2 - Patrons'),
        (3, 'Level 3 - Conference Chairs'),
        (4, 'Level 4 - Program Chairs'),
        (5, 'Level 5 - Technical Chairs'),
        (6, 'Level 6 - Organizing Committee'),
        (7, 'Level 7 - Other Chairs'),
        (8, 'Level 8 - Committee Members'),
    ]
    
    name = models.CharField(max_length=200)
    title = models.CharField(max_length=300)
    organization = models.CharField(max_length=300)
    image = models.ImageField(upload_to='committee/', blank=True, null=True)
    order = models.IntegerField(default=0, help_text="Display order within the same role/level")
    role = models.CharField(max_length=50, choices=ROLE_CHOICES, default='member', help_text="Committee role/position")
    hierarchy_level = models.IntegerField(choices=HIERARCHY_LEVELS, default=8, help_text="Hierarchical level for organization")
    email = models.EmailField(blank=True, help_text="Contact email")
    phone = models.CharField(max_length=20, blank=True, help_text="Contact phone")
    bio = models.TextField(blank=True, help_text="Short biography")
    is_active = models.BooleanField(default=True, help_text="Display on committee page")
    
    class Meta:
        ordering = ['hierarchy_level', 'order', 'name']
        
    def __str__(self):
        return f"{self.name} - {self.get_role_display()}"
    
    def get_role_css_class(self):
        """Return CSS class based on role for styling"""
        role_classes = {
            'chief_patron': 'chief-patron',
            'patron': 'patron',
            'chair': 'chair',
            'co_chair': 'co-chair',
            'program_chair': 'program-chair',
            'technical_chair': 'technical-chair',
            'organizing_chair': 'organizing-chair',
            'organizing_co_chair': 'organizing-co-chair',
            'organizing_secretary': 'organizing-secretary',
            'publication_chair': 'publication-chair',
            'registration_chair': 'registration-chair',
            'publicity_chair': 'publicity-chair',
            'finance_chair': 'finance-chair',
            'local_arrangement': 'local-arrangement',
            'member': 'member',
        }
        return role_classes.get(self.role, 'member')

class ConferenceTrack(models.Model):
    TRACK_TYPES = [
        ('regular', 'Regular Track'),
        ('special', 'Special Session/Track'),
    ]
    
    track_number = models.IntegerField()
    title = models.CharField(max_length=500)
    description = models.TextField(blank=True)
    track_type = models.CharField(max_length=20, choices=TRACK_TYPES, default='regular')
    track_chair = models.CharField(max_length=200, blank=True)
    image = models.ImageField(upload_to='tracks/', blank=True, null=True)
    
    class Meta:
        ordering = ['track_number']
    
    def __str__(self):
        return f"Track {self.track_number}: {self.title}"

class TouristAttraction(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    image = models.ImageField(upload_to='attractions/', blank=True, null=True)
    location_url = models.URLField(blank=True)
    order = models.IntegerField(default=0)
    
    class Meta:
        ordering = ['order']
    
    def __str__(self):
        return self.name

class ImportantDate(models.Model):
    event = models.CharField(max_length=200)
    date = models.DateField()
    description = models.TextField(blank=True)
    order = models.IntegerField(default=0)
    
    class Meta:
        ordering = ['order', 'date']
    
    def __str__(self):
        return f"{self.event} - {self.date}"

class Slider(models.Model):
    title = models.CharField(max_length=200, blank=True)
    image = models.ImageField(upload_to='slider/')
    order = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        ordering = ['order']
    
    def __str__(self):
        return self.title or f"Slide {self.id}"

class ConferenceSettings(models.Model):
    site_title = models.CharField(max_length=200, default="ICCCA 2025")
    conference_dates = models.CharField(max_length=100, default="November 28-30, 2025")
    location = models.CharField(max_length=300, default="Galgotias University, Greater Noida, India")
    about_text = models.TextField()
    conference_objective = models.TextField()
    brochure_pdf = models.FileField(upload_to='documents/', blank=True, null=True)
    
    class Meta:
        verbose_name = "Conference Settings"
        verbose_name_plural = "Conference Settings"
    
    def __str__(self):
        return self.site_title

class Sponsor(models.Model):
    name = models.CharField(max_length=200)
    logo = models.ImageField(upload_to='sponsors/')
    website = models.URLField(blank=True)
    order = models.IntegerField(default=0)
    
    class Meta:
        ordering = ['order']
    
    def __str__(self):
        return self.name

# Blog Post Models
class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name_plural = 'Categories'
        ordering = ['name']
    
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('conference:blog_category', kwargs={'slug': self.slug})

class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=50, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['name']
    
    def __str__(self):
        return self.name

class BlogPost(models.Model):
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('published', 'Published'),
        ('archived', 'Archived'),
    ]
    
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blog_posts')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='posts')
    tags = models.ManyToManyField(Tag, blank=True, related_name='posts')
    
    excerpt = models.TextField(max_length=300, help_text='Brief description of the post')
    content = models.TextField()
    
    featured_image = models.ImageField(upload_to='blog/images/', blank=True, null=True)
    
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')
    featured = models.BooleanField(default=False, help_text='Mark as featured post')
    
    meta_description = models.CharField(max_length=160, blank=True, help_text='SEO meta description')
    meta_keywords = models.CharField(max_length=200, blank=True, help_text='SEO keywords, comma separated')
    
    views = models.PositiveIntegerField(default=0)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    published_at = models.DateTimeField(blank=True, null=True)
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['-created_at']),
            models.Index(fields=['status']),
            models.Index(fields=['featured']),
        ]
    
    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('conference:blog_detail', kwargs={'slug': self.slug})
    
    def save(self, *args, **kwargs):
        if self.status == 'published' and not self.published_at:
            self.published_at = timezone.now()
        
        super().save(*args, **kwargs)
        
        # Resize featured image if it exists
        if self.featured_image:
            img_path = self.featured_image.path
            if os.path.exists(img_path):
                with Image.open(img_path) as img:
                    if img.height > 600 or img.width > 800:
                        img.thumbnail((800, 600), Image.Resampling.LANCZOS)
                        img.save(img_path, optimize=True, quality=85)
    
    def increment_views(self):
        self.views += 1
        self.save(update_fields=['views'])
    
    @property
    def reading_time(self):
        word_count = len(self.content.split())
        return max(1, word_count // 200)  # Assuming 200 words per minute

class Comment(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('spam', 'Spam'),
    ]
    
    post = models.ForeignKey(BlogPost, on_delete=models.CASCADE, related_name='comments')
    name = models.CharField(max_length=100)
    email = models.EmailField()
    website = models.URLField(blank=True)
    content = models.TextField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    ip_address = models.GenericIPAddressField(blank=True, null=True)
    user_agent = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['status']),
            models.Index(fields=['-created_at']),
        ]
    
    def __str__(self):
        return f'Comment by {self.name} on {self.post.title}'

# Newsletter Subscription Model
class Newsletter(models.Model):
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=100, blank=True)
    subscribed_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        ordering = ['-subscribed_at']
    
    def __str__(self):
        return self.email

class MaintenanceMode(models.Model):
    """Site-wide or page-specific maintenance mode"""
    MAINTENANCE_TYPES = [
        ('site', 'Entire Site'),
        ('page', 'Specific Page'),
        ('feature', 'Specific Feature'),
    ]
    
    title = models.CharField(max_length=200, default="Site Under Maintenance")
    message = models.TextField(default="We're currently performing scheduled maintenance. Please check back soon!")
    maintenance_type = models.CharField(max_length=20, choices=MAINTENANCE_TYPES, default='site')
    page_url = models.CharField(max_length=200, blank=True, help_text="For page-specific maintenance, specify the URL pattern")
    is_active = models.BooleanField(default=False)
    start_time = models.DateTimeField(null=True, blank=True)
    end_time = models.DateTimeField(null=True, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.get_maintenance_type_display()}: {self.title}"
    
    def is_currently_active(self):
        if not self.is_active:
            return False
        
        now = timezone.now()
        
        if self.start_time and now < self.start_time:
            return False
            
        if self.end_time and now > self.end_time:
            return False
            
        return True
    
    class Meta:
        ordering = ['-created_at']

class Notice(models.Model):
    """Admin notices displayed on the home page"""
    NOTICE_TYPES = [
        ('info', 'Information'),
        ('warning', 'Warning'),
        ('success', 'Success'),
        ('danger', 'Important Alert'),
        ('primary', 'Announcement'),
    ]
    
    title = models.CharField(max_length=200)
    content = models.TextField()
    notice_type = models.CharField(max_length=20, choices=NOTICE_TYPES, default='info')
    is_active = models.BooleanField(default=True)
    is_urgent = models.BooleanField(default=False, help_text="Urgent notices appear at the top")
    start_date = models.DateTimeField(default=timezone.now)
    end_date = models.DateTimeField(null=True, blank=True, help_text="Leave blank for permanent notice")
    show_on_pages = models.TextField(
        blank=True,
        help_text="Comma-separated list of pages to show on (e.g., home,blog,contact). Leave blank for all pages"
    )
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.title
    
    def is_currently_active(self):
        if not self.is_active:
            return False
            
        now = timezone.now()
        
        if now < self.start_date:
            return False
            
        if self.end_date and now > self.end_date:
            return False
            
        return True
    
    def get_display_pages(self):
        if not self.show_on_pages:
            return ['all']
        return [page.strip() for page in self.show_on_pages.split(',')]
    
    class Meta:
        ordering = ['-is_urgent', '-created_at']

class Timeline(models.Model):
    """Conference timeline and milestones management"""
    TIMELINE_TYPES = [
        ('important_date', 'Important Date'),
        ('submission_deadline', 'Submission Deadline'),
        ('notification', 'Notification'),
        ('registration', 'Registration'),
        ('event', 'Conference Event'),
        ('milestone', 'General Milestone'),
    ]
    
    STATUS_CHOICES = [
        ('upcoming', 'Upcoming'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
        ('extended', 'Extended'),
    ]
    
    title = models.CharField(max_length=200)
    description = models.TextField()
    timeline_type = models.CharField(max_length=50, choices=TIMELINE_TYPES, default='milestone')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='upcoming')
    date = models.DateTimeField()
    end_date = models.DateTimeField(null=True, blank=True, help_text="For events with duration")
    is_featured = models.BooleanField(default=False, help_text="Display prominently on homepage")
    is_public = models.BooleanField(default=True, help_text="Visible to public")
    icon = models.CharField(max_length=50, default='fas fa-calendar', help_text="FontAwesome icon class")
    color = models.CharField(max_length=7, default='#a0352f', help_text="Hex color code")
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.title} - {self.date.strftime('%Y-%m-%d')}"
    
    def is_overdue(self):
        return self.date < timezone.now() and self.status == 'upcoming'
    
    def days_remaining(self):
        if self.status in ['completed', 'cancelled']:
            return 0
        delta = self.date - timezone.now()
        return max(0, delta.days)
    
    def is_current(self):
        now = timezone.now()
        if self.end_date:
            return self.date <= now <= self.end_date
        return self.date.date() == now.date()
    
    class Meta:
        ordering = ['date']

class StatusUpdate(models.Model):
    """Conference status updates and announcements"""
    UPDATE_TYPES = [
        ('general', 'General Update'),
        ('important', 'Important Announcement'),
        ('deadline', 'Deadline Reminder'),
        ('event', 'Event Update'),
        ('technical', 'Technical Information'),
        ('registration', 'Registration Update'),
    ]
    
    PRIORITY_LEVELS = [
        ('low', 'Low Priority'),
        ('medium', 'Medium Priority'),
        ('high', 'High Priority'),
        ('urgent', 'Urgent'),
    ]
    
    title = models.CharField(max_length=200)
    content = models.TextField()
    update_type = models.CharField(max_length=50, choices=UPDATE_TYPES, default='general')
    priority = models.CharField(max_length=20, choices=PRIORITY_LEVELS, default='medium')
    is_published = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False, help_text="Show on homepage")
    publish_date = models.DateTimeField(default=timezone.now)
    expire_date = models.DateTimeField(null=True, blank=True, help_text="Auto-hide after this date")
    related_timeline = models.ForeignKey(Timeline, on_delete=models.SET_NULL, null=True, blank=True, 
                                       help_text="Link to related timeline item")
    tags = models.CharField(max_length=200, blank=True, help_text="Comma-separated tags")
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.title} ({self.get_priority_display()})"
    
    def is_active(self):
        if not self.is_published:
            return False
        if self.expire_date and timezone.now() > self.expire_date:
            return False
        return timezone.now() >= self.publish_date
    
    def get_tags_list(self):
        return [tag.strip() for tag in self.tags.split(',') if tag.strip()]
    
    def is_recent(self):
        return (timezone.now() - self.created_at).days <= 7
    
    class Meta:
        ordering = ['-priority', '-created_at']

class Schedule(models.Model):
    """Conference schedule and program management"""
    SCHEDULE_TYPES = [
        ('keynote', 'Keynote Speech'),
        ('presentation', 'Paper Presentation'),
        ('panel', 'Panel Discussion'),
        ('workshop', 'Workshop'),
        ('break', 'Break'),
        ('lunch', 'Lunch'),
        ('registration', 'Registration'),
        ('ceremony', 'Ceremony'),
        ('networking', 'Networking Event'),
        ('other', 'Other Event'),
    ]
    
    DAYS = [
        ('day1', 'Day 1'),
        ('day2', 'Day 2'),
        ('day3', 'Day 3'),
        ('day4', 'Day 4'),
        ('day5', 'Day 5'),
    ]
    
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    schedule_type = models.CharField(max_length=50, choices=SCHEDULE_TYPES, default='presentation')
    speaker = models.CharField(max_length=200, blank=True, help_text="Speaker name(s)")
    location = models.CharField(max_length=100, blank=True, help_text="Room/Hall/Venue")
    day = models.CharField(max_length=10, choices=DAYS, default='day1')
    start_time = models.TimeField()
    end_time = models.TimeField()
    date = models.DateField(help_text="Conference date for this schedule item")
    is_featured = models.BooleanField(default=False, help_text="Highlight this session")
    is_published = models.BooleanField(default=True, help_text="Visible to public")
    session_chair = models.CharField(max_length=200, blank=True)
    track = models.CharField(max_length=100, blank=True, help_text="Conference track/theme")
    capacity = models.PositiveIntegerField(null=True, blank=True, help_text="Maximum attendees")
    requirements = models.TextField(blank=True, help_text="Special requirements or notes")
    color = models.CharField(max_length=7, default='#a0352f', help_text="Display color")
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.get_day_display()} - {self.start_time.strftime('%H:%M')} - {self.title}"
    
    def duration_minutes(self):
        """Calculate session duration in minutes"""
        from datetime import datetime, timedelta
        start = datetime.combine(datetime.today(), self.start_time)
        end = datetime.combine(datetime.today(), self.end_time)
        if end > start:
            return int((end - start).total_seconds() / 60)
        return 0
    
    @property
    def is_active(self):
        """Alias for is_published for consistency with template"""
        return self.is_published
    
    @property 
    def venue(self):
        """Alias for location for consistency with template"""
        return self.location
        duration = end - start
        return int(duration.total_seconds() / 60)
    
    def is_current_session(self):
        """Check if this session is currently active"""
        from django.utils import timezone
        now = timezone.now()
        today = now.date()
        current_time = now.time()
        
        return (self.date == today and 
                self.start_time <= current_time <= self.end_time)
    
    def is_upcoming_today(self):
        """Check if this session is upcoming today"""
        from django.utils import timezone
        now = timezone.now()
        today = now.date()
        current_time = now.time()
        
        return (self.date == today and 
                current_time < self.start_time)
    
    def time_until_start(self):
        """Get time until session starts (if upcoming today)"""
        from django.utils import timezone
        from datetime import datetime, timedelta
        
        now = timezone.now()
        today = now.date()
        
        if self.date == today:
            start_datetime = datetime.combine(self.date, self.start_time)
            current_datetime = datetime.combine(today, now.time())
            
            if start_datetime > current_datetime:
                delta = start_datetime - current_datetime
                hours = delta.seconds // 3600
                minutes = (delta.seconds % 3600) // 60
                return f"{hours}h {minutes}m"
        return None
    
    class Meta:
        ordering = ['date', 'start_time']

class Speaker(models.Model):
    """Conference speakers and keynote speakers management"""
    SPEAKER_TYPES = [
        ('keynote', 'Keynote Speaker'),
        ('invited', 'Invited Speaker'),
        ('panel', 'Panel Speaker'),
        ('workshop', 'Workshop Speaker'),
        ('regular', 'Regular Speaker'),
    ]
    
    # Basic Information
    name = models.CharField(max_length=200)
    title = models.CharField(max_length=300, help_text="Professional title/position")
    organization = models.CharField(max_length=300, help_text="University/Company/Institution")
    country = models.CharField(max_length=100, blank=True)
    
    # Profile Information
    bio = models.TextField(help_text="Speaker biography")
    expertise = models.CharField(max_length=500, blank=True, help_text="Areas of expertise (comma-separated)")
    photo = models.ImageField(upload_to='speakers/', blank=True, null=True)
    
    # Speaker Details
    speaker_type = models.CharField(max_length=20, choices=SPEAKER_TYPES, default='regular')
    talk_title = models.CharField(max_length=300, blank=True, help_text="Title of the talk/presentation")
    talk_abstract = models.TextField(blank=True, help_text="Abstract of the talk")
    session_time = models.CharField(max_length=100, blank=True, help_text="e.g., 'Day 1, 10:00 AM'")
    
    # Social and Contact
    email = models.EmailField(blank=True)
    website = models.URLField(blank=True)
    linkedin = models.URLField(blank=True)
    twitter = models.CharField(max_length=100, blank=True, help_text="Twitter handle (without @)")
    orcid = models.CharField(max_length=100, blank=True, help_text="ORCID ID")
    
    # Display Settings
    is_featured = models.BooleanField(default=False, help_text="Show on homepage")
    is_published = models.BooleanField(default=True, help_text="Visible to public")
    display_order = models.PositiveIntegerField(default=0, help_text="Order of display (lower numbers first)")
    
    # Administrative
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.name} ({self.get_speaker_type_display()})"
    
    def get_expertise_list(self):
        """Get list of expertise areas"""
        return [item.strip() for item in self.expertise.split(',') if item.strip()]
    
    def get_social_links(self):
        """Get dictionary of social links"""
        links = {}
        if self.website:
            links['website'] = self.website
        if self.linkedin:
            links['linkedin'] = self.linkedin
        if self.twitter:
            links['twitter'] = f"https://twitter.com/{self.twitter.lstrip('@')}"
        if self.email:
            links['email'] = f"mailto:{self.email}"
        if self.orcid:
            links['orcid'] = f"https://orcid.org/{self.orcid}"
        return links
    
    def get_photo_url(self):
        """Get photo URL or default placeholder"""
        if self.photo and hasattr(self.photo, 'url'):
            return self.photo.url
        return '/static/images/default-person.svg'
    
    class Meta:
        ordering = ['display_order', 'name']


class AdminRole(models.Model):
    """Admin roles for role-based access control"""
    ROLE_TYPES = [
        ('super_admin', 'Super Administrator'),
        ('content_admin', 'Content Administrator'),
        ('user_admin', 'User Administrator'),
        ('blog_admin', 'Blog Administrator'),
        ('event_admin', 'Event Administrator'),
        ('schedule_admin', 'Schedule Administrator'),
        ('speaker_admin', 'Speaker Administrator'),
        ('committee_admin', 'Committee Administrator'),
        ('notice_admin', 'Notice Administrator'),
        ('timeline_admin', 'Timeline Administrator'),
        ('readonly_admin', 'Read Only Administrator'),
    ]
    
    name = models.CharField(max_length=100, unique=True)
    role_type = models.CharField(max_length=50, choices=ROLE_TYPES, unique=True)
    description = models.TextField(help_text="Description of role permissions")
    
    # Dashboard access permissions
    can_access_dashboard = models.BooleanField(default=True)
    can_manage_users = models.BooleanField(default=False)
    can_manage_content = models.BooleanField(default=False)
    can_manage_blog = models.BooleanField(default=False)
    can_manage_events = models.BooleanField(default=False)
    can_manage_schedule = models.BooleanField(default=False)
    can_manage_speakers = models.BooleanField(default=False)
    can_manage_committee = models.BooleanField(default=False)
    can_manage_notices = models.BooleanField(default=False)
    can_manage_timeline = models.BooleanField(default=False)
    can_export_data = models.BooleanField(default=False)
    can_view_logs = models.BooleanField(default=False)
    
    # System permissions
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['name']


class UserProfile(models.Model):
    """Extended user profile with admin roles"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    admin_role = models.ForeignKey(AdminRole, on_delete=models.SET_NULL, null=True, blank=True)
    
    # Additional profile information
    phone = models.CharField(max_length=20, blank=True)
    department = models.CharField(max_length=100, blank=True)
    position = models.CharField(max_length=100, blank=True)
    bio = models.TextField(blank=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    
    # Access control
    is_admin_user = models.BooleanField(default=False, help_text="Can access admin dashboard")
    last_login_ip = models.GenericIPAddressField(null=True, blank=True)
    failed_login_attempts = models.PositiveIntegerField(default=0)
    account_locked_until = models.DateTimeField(null=True, blank=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.user.get_full_name() or self.user.username} - {self.admin_role or 'No Role'}"
    
    def has_permission(self, permission):
        """Check if user has specific permission"""
        if self.user.is_superuser:
            return True
        if not self.admin_role or not self.admin_role.is_active:
            return False
        return getattr(self.admin_role, permission, False)
    
    def get_avatar_url(self):
        """Get avatar URL with fallback"""
        if self.avatar:
            return self.avatar.url
        return '/static/images/default-avatar.svg'
    
    class Meta:
        ordering = ['-created_at']


class UserSession(models.Model):
    """Track user sessions for security"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sessions')
    session_key = models.CharField(max_length=40, unique=True)
    ip_address = models.GenericIPAddressField()
    user_agent = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    last_activity = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return f"{self.user.username} - {self.ip_address}"
    
    class Meta:
        ordering = ['-last_activity']
