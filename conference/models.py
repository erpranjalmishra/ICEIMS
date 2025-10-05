from django.db import models
from django.utils.text import slugify
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone
from PIL import Image
import os

class HierarchyLevel(models.Model):
    """Customizable hierarchy level names for committee organization"""
    level_number = models.IntegerField(unique=True, help_text="Level number (e.g., 1, 2, 3, etc.) - Lower numbers appear first")
    level_name = models.CharField(max_length=200, help_text="Custom name for this level (e.g., 'Chief Patron', 'Patrons', 'Advisory Board', etc.)")
    description = models.TextField(blank=True, help_text="Optional description of this level")
    is_active = models.BooleanField(default=True, help_text="Whether this level is displayed on the website")
    
    class Meta:
        ordering = ['level_number']
        verbose_name = "Hierarchy Level"
        verbose_name_plural = "Hierarchy Levels"
    
    def __str__(self):
        return f"Level {self.level_number}: {self.level_name}"
    
    @classmethod
    def get_level_choices(cls):
        """Get all active hierarchy levels as choices for CommitteeMember"""
        levels = cls.objects.filter(is_active=True).order_by('level_number')
        if levels.exists():
            return [(level.level_number, f"Level {level.level_number} - {level.level_name}") for level in levels]
        # Fallback to default if no custom levels exist
        return [
            (1, 'Level 1 - Chief Patron'),
            (2, 'Level 2 - Patrons'),
            (3, 'Level 3 - Conference Chairs'),
            (4, 'Level 4 - Program Chairs'),
            (5, 'Level 5 - Technical Chairs'),
            (6, 'Level 6 - Organizing Committee'),
            (7, 'Level 7 - Other Chairs'),
            (8, 'Level 8 - Committee Members'),
        ]
    
    @classmethod
    def get_level_name(cls, level_number):
        """Get the custom name for a specific level number"""
        try:
            level = cls.objects.get(level_number=level_number, is_active=True)
            return level.level_name
        except cls.DoesNotExist:
            # Fallback to default names
            default_names = {
                1: 'Chief Patron',
                2: 'Patrons',
                3: 'Conference Chairs',
                4: 'Program Chairs',
                5: 'Technical Chairs',
                6: 'Organizing Committee',
                7: 'Other Chairs',
                8: 'Committee Members',
            }
            return default_names.get(level_number, f'Level {level_number}')

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
    hierarchy_level = models.IntegerField(default=8, help_text="Hierarchical level for organization (managed in Hierarchy Levels)")
    email = models.EmailField(blank=True, help_text="Contact email")
    phone = models.CharField(max_length=20, blank=True, help_text="Contact phone")
    bio = models.TextField(blank=True, help_text="Short biography")
    is_active = models.BooleanField(default=True, help_text="Display on committee page")
    
    class Meta:
        ordering = ['hierarchy_level', 'order', 'name']
        
    def __str__(self):
        return f"{self.name} - {self.get_role_display()}"
    
    def get_hierarchy_level_name(self):
        """Get the custom hierarchy level name"""
        return HierarchyLevel.get_level_name(self.hierarchy_level)
    
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
    
    track_number = models.IntegerField(help_text="Track number for ordering")
    title = models.CharField(max_length=500, help_text="Track title/name")
    description = models.TextField(blank=True, help_text="Track topics - one per line")
    track_type = models.CharField(max_length=20, choices=TRACK_TYPES, default='regular')
    track_chair = models.CharField(max_length=200, blank=True, help_text="Track chair name(s)")
    image = models.ImageField(upload_to='tracks/', blank=True, null=True, help_text="Track image/icon")
    
    # New fields for better management
    is_active = models.BooleanField(default=True, help_text="Display on website")
    display_order = models.IntegerField(default=0, help_text="Custom display order (overrides track_number)")
    color = models.CharField(max_length=7, default='#a0352f', help_text="Display color (hex code)")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['display_order', 'track_number']
    
    def __str__(self):
        return f"Track {self.track_number}: {self.title}"
    
    def get_topics_list(self):
        """Get list of topics from description"""
        return [line.strip() for line in self.description.splitlines() if line.strip()]
    
    def topic_count(self):
        """Count the number of topics"""
        return len(self.get_topics_list())

class TouristAttraction(models.Model):
    CATEGORY_CHOICES = [
        ('historic', 'Historic'),
        ('memorial', 'Memorial'),
        ('spiritual', 'Spiritual'),
        ('temple', 'Temple'),
        ('unesco', 'UNESCO Site'),
        ('entertainment', 'Entertainment'),
        ('shopping', 'Shopping'),
        ('wonder', 'Wonder of World'),
        ('garden', 'Garden'),
        ('market', 'Market'),
    ]
    
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=250, unique=True, blank=True)
    description = models.TextField()
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='historic')
    image = models.ImageField(upload_to='attractions/', blank=True, null=True)
    image_url = models.URLField(blank=True, help_text="External image URL (used if no image uploaded)")
    location_url = models.URLField(blank=True, help_text="Google Maps URL")
    map_embed = models.TextField(blank=True, help_text="Google Maps embed iframe code")
    guide_link = models.URLField(blank=True, help_text="Link to detailed guide/blog page")
    distance = models.CharField(max_length=50, blank=True, help_text="Distance from KIET (e.g., '45 km')")
    time_required = models.CharField(max_length=50, blank=True, help_text="Time required to visit (e.g., '2-3 hours')")
    rating = models.DecimalField(max_digits=2, decimal_places=1, default=4.5, help_text="Rating out of 5")
    is_featured = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    order = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['order', 'name']
        verbose_name = "Tourist Attraction"
        verbose_name_plural = "Tourist Attractions"
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

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
    PARTNERSHIP_TYPES = [
        ('sponsorship', 'Sponsorship'),
        ('partnership', 'Partnership'),
    ]
    
    SPONSORSHIP_TIERS = [
        ('', 'None (Not Applicable)'),
        ('platinum', 'Platinum Sponsor'),
        ('gold', 'Gold Sponsor'),
        ('silver', 'Silver Sponsor'),
        ('bronze', 'Bronze Sponsor'),
    ]
    
    PARTNER_TYPES = [
        ('', 'None (Not Applicable)'),
        ('academic', 'Academic Partner'),
        ('technology', 'Technology Partner'),
        ('media', 'Media Partner'),
        ('industry', 'Industry Partner'),
        ('institutional', 'Institutional Partner'),
    ]
    
    name = models.CharField(max_length=200)
    logo = models.ImageField(upload_to='sponsors/')
    website = models.URLField(blank=True)
    
    # New fields for partnership type
    partnership_type = models.CharField(
        max_length=20, 
        choices=PARTNERSHIP_TYPES, 
        default='sponsorship',
        help_text="Select whether this is a sponsorship or partnership"
    )
    
    # Sponsorship tier (only applicable when partnership_type is 'sponsorship')
    sponsorship_tier = models.CharField(
        max_length=20, 
        choices=SPONSORSHIP_TIERS, 
        blank=True,
        default='',
        help_text="Select sponsorship tier (only for sponsors)"
    )
    
    # Partner type (only applicable when partnership_type is 'partnership')
    partner_type = models.CharField(
        max_length=20, 
        choices=PARTNER_TYPES, 
        blank=True,
        default='',
        help_text="Select partner type (only for partners)"
    )
    
    description = models.TextField(blank=True, help_text="Brief description of the sponsor/partner")
    order = models.IntegerField(default=0, help_text="Display order within the same tier/type")
    is_active = models.BooleanField(default=True, help_text="Display on website")
    
    class Meta:
        ordering = ['partnership_type', 'sponsorship_tier', 'partner_type', 'order']
    
    def __str__(self):
        if self.partnership_type == 'sponsorship' and self.sponsorship_tier:
            return f"{self.name} ({self.get_sponsorship_tier_display()})"
        elif self.partnership_type == 'partnership' and self.partner_type:
            return f"{self.name} ({self.get_partner_type_display()})"
        return self.name
    
    def get_display_category(self):
        """Get the display category for grouping"""
        if self.partnership_type == 'sponsorship':
            return self.get_sponsorship_tier_display() if self.sponsorship_tier else 'Sponsor'
        elif self.partnership_type == 'partnership':
            return self.get_partner_type_display() if self.partner_type else 'Partner'
        return 'Other'

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
    link_url = models.URLField(blank=True, help_text="Optional link URL for 'Read More' or 'Learn More' button")
    link_text = models.CharField(max_length=100, blank=True, default="Read More", help_text="Text for the link button")
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
    can_manage_tracks = models.BooleanField(default=False, help_text="Permission to manage conference tracks")
    can_manage_attractions = models.BooleanField(default=False, help_text="Permission to manage tourist attractions")
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
    phone = models.CharField(max_length=20, blank=True, default='')
    department = models.CharField(max_length=100, blank=True, default='')
    position = models.CharField(max_length=100, blank=True, default='')
    bio = models.TextField(blank=True, default='')
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


class EmailTemplate(models.Model):
    """Email templates for automated emails"""
    TEMPLATE_TYPES = [
        ('welcome', 'Welcome Email'),
        ('login_notification', 'Login Notification'),
        ('security_alert', 'Security Alert'),
        ('password_reset', 'Password Reset'),
        ('otp_verification', 'OTP Verification'),
        ('account_created', 'Account Created'),
        ('role_assigned', 'Role Assigned'),
        ('permission_changed', 'Permission Changed'),
        ('data_export', 'Data Export Notification'),
        ('custom', 'Custom Email'),
    ]
    
    name = models.CharField(max_length=200, unique=True)
    template_type = models.CharField(max_length=50, choices=TEMPLATE_TYPES)
    subject = models.CharField(max_length=300)
    body_html = models.TextField(help_text="HTML content with template variables")
    body_text = models.TextField(help_text="Plain text fallback", blank=True)
    is_active = models.BooleanField(default=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # Template variables help text
    variables_help = models.TextField(
        default="Available variables: {{user_name}}, {{email}}, {{site_name}}, {{login_time}}, {{ip_address}}, {{action}}",
        help_text="List of available template variables"
    )
    
    def __str__(self):
        return f"{self.name} ({self.get_template_type_display()})"
    
    class Meta:
        ordering = ['template_type', 'name']


class EmailLog(models.Model):
    """Log all sent emails for tracking and debugging"""
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('sent', 'Sent'),
        ('failed', 'Failed'),
        ('bounced', 'Bounced'),
    ]
    
    recipient = models.EmailField()
    recipient_user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    subject = models.CharField(max_length=300)
    body = models.TextField()
    template = models.ForeignKey(EmailTemplate, on_delete=models.SET_NULL, null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    error_message = models.TextField(blank=True)
    
    # Tracking
    sent_at = models.DateTimeField(null=True, blank=True)
    opened_at = models.DateTimeField(null=True, blank=True)
    clicked_at = models.DateTimeField(null=True, blank=True)
    
    # Metadata
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.recipient} - {self.subject} ({self.status})"
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['recipient']),
            models.Index(fields=['status']),
            models.Index(fields=['-created_at']),
        ]


class OTPVerification(models.Model):
    """OTP verification for secure login"""
    OTP_PURPOSES = [
        ('login', 'Login Verification'),
        ('password_reset', 'Password Reset'),
        ('email_change', 'Email Change'),
        ('sensitive_action', 'Sensitive Action'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='otp_codes')
    otp_code = models.CharField(max_length=10)
    purpose = models.CharField(max_length=50, choices=OTP_PURPOSES, default='login')
    is_verified = models.BooleanField(default=False)
    is_used = models.BooleanField(default=False)
    
    # Security
    attempts = models.IntegerField(default=0)
    max_attempts = models.IntegerField(default=3)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    
    # Timing
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    verified_at = models.DateTimeField(null=True, blank=True)
    
    def __str__(self):
        return f"{self.user.username} - {self.purpose} - {self.otp_code}"
    
    def is_valid(self):
        """Check if OTP is still valid"""
        if self.is_used or self.is_verified:
            return False
        if timezone.now() > self.expires_at:
            return False
        if self.attempts >= self.max_attempts:
            return False
        return True
    
    def verify(self, code):
        """Verify OTP code"""
        self.attempts += 1
        if self.otp_code == code and self.is_valid():
            self.is_verified = True
            self.is_used = True
            self.verified_at = timezone.now()
            self.save()
            return True
        self.save()
        return False
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user', 'is_verified']),
            models.Index(fields=['expires_at']),
        ]


class SecurityEvent(models.Model):
    """Log security-related events"""
    EVENT_TYPES = [
        ('login', 'User Login'),
        ('login_failed', 'Failed Login Attempt'),
        ('logout', 'User Logout'),
        ('password_change', 'Password Changed'),
        ('email_change', 'Email Changed'),
        ('role_change', 'Role Changed'),
        ('permission_change', 'Permission Changed'),
        ('account_locked', 'Account Locked'),
        ('account_unlocked', 'Account Unlocked'),
        ('otp_sent', 'OTP Sent'),
        ('otp_verified', 'OTP Verified'),
        ('otp_failed', 'OTP Failed'),
        ('data_export', 'Data Exported'),
        ('suspicious_activity', 'Suspicious Activity'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='security_events')
    event_type = models.CharField(max_length=50, choices=EVENT_TYPES)
    description = models.TextField()
    
    # Context
    ip_address = models.GenericIPAddressField()
    user_agent = models.TextField(blank=True)
    location = models.CharField(max_length=200, blank=True, help_text="Geo-location if available")
    
    # Notification
    email_sent = models.BooleanField(default=False)
    email_sent_at = models.DateTimeField(null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.user.username} - {self.get_event_type_display()} - {self.created_at}"
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user', '-created_at']),
            models.Index(fields=['event_type']),
        ]


class EmailCampaign(models.Model):
    """Email campaigns for bulk sending"""
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('scheduled', 'Scheduled'),
        ('sending', 'Sending'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
    
    name = models.CharField(max_length=200)
    subject = models.CharField(max_length=300)
    body_html = models.TextField()
    body_text = models.TextField(blank=True)
    
    # Recipients
    recipient_filter = models.CharField(
        max_length=50,
        choices=[
            ('all_users', 'All Users'),
            ('admin_users', 'Admin Users'),
            ('subscribers', 'Newsletter Subscribers'),
            ('custom', 'Custom List'),
        ],
        default='all_users'
    )
    custom_recipients = models.TextField(blank=True, help_text="Email addresses, one per line")
    
    # Scheduling
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    scheduled_at = models.DateTimeField(null=True, blank=True)
    started_at = models.DateTimeField(null=True, blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    
    # Statistics
    total_recipients = models.IntegerField(default=0)
    sent_count = models.IntegerField(default=0)
    failed_count = models.IntegerField(default=0)
    opened_count = models.IntegerField(default=0)
    clicked_count = models.IntegerField(default=0)
    
    # Management
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.name} ({self.get_status_display()})"

    class Meta:
        ordering = ['-created_at']


class ScheduledEmail(models.Model):
    """Scheduled emails to be sent at a specific time"""
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('sent', 'Sent'),
        ('failed', 'Failed'),
        ('cancelled', 'Cancelled'),
    ]
    
    RECIPIENT_TYPES = [
        ('all_users', 'All Users'),
        ('all_staff', 'All Staff'),
        ('all_reviewers', 'All Reviewers'),
        ('all_authors', 'All Authors'),
        ('specific', 'Specific Emails'),
        ('user_group', 'User Group'),
    ]
    
    template = models.ForeignKey(EmailTemplate, on_delete=models.CASCADE, related_name='scheduled_sends')
    recipient_type = models.CharField(max_length=50, choices=RECIPIENT_TYPES)
    recipient_emails = models.TextField(blank=True, help_text="Comma-separated email addresses for specific recipients")
    recipient_count = models.IntegerField(default=0)
    
    scheduled_time = models.DateTimeField()
    sent_time = models.DateTimeField(null=True, blank=True)
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    error_message = models.TextField(blank=True)
    
    emails_sent = models.IntegerField(default=0)
    emails_failed = models.IntegerField(default=0)
    
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.template.name} - Scheduled for {self.scheduled_time}"
    
    class Meta:
        ordering = ['scheduled_time']
        verbose_name = 'Scheduled Email'
        verbose_name_plural = 'Scheduled Emails'


class UniversityInfo(models.Model):
    """University information for About Galgotias University section"""
    # Basic Information
    name = models.CharField(max_length=200, default="Galgotias University")
    tagline = models.CharField(max_length=500, blank=True, help_text="University tagline/motto")
    
    # Main Content
    about_text = models.TextField(help_text="Main about text for homepage")
    full_description = models.TextField(help_text="Detailed description for dedicated page")
    
    # Statistics
    student_count = models.CharField(max_length=20, default="30K+", help_text="e.g., 30K+")
    school_count = models.CharField(max_length=20, default="20", help_text="Number of schools")
    program_count = models.CharField(max_length=20, default="200+", help_text="Number of programs")
    faculty_count = models.CharField(max_length=20, blank=True, help_text="Number of faculty members")
    campus_area = models.CharField(max_length=50, blank=True, help_text="e.g., '52 acres'")
    established_year = models.CharField(max_length=4, default="2011", help_text="Year established")
    
    # Location
    address = models.TextField(blank=True)
    city = models.CharField(max_length=100, default="Greater Noida")
    state = models.CharField(max_length=100, default="Uttar Pradesh")
    country = models.CharField(max_length=100, default="India")
    pincode = models.CharField(max_length=10, blank=True)
    
    # Contact
    phone = models.CharField(max_length=50, blank=True)
    email = models.EmailField(blank=True)
    website = models.URLField(blank=True)
    
    # Social Media
    facebook_url = models.URLField(blank=True)
    twitter_url = models.URLField(blank=True)
    linkedin_url = models.URLField(blank=True)
    instagram_url = models.URLField(blank=True)
    youtube_url = models.URLField(blank=True)
    
    # Features & Highlights
    key_features = models.TextField(
        blank=True, 
        help_text="Key features, one per line. These will be displayed as bullet points."
    )
    accreditations = models.TextField(
        blank=True,
        help_text="Accreditations and rankings, one per line"
    )
    
    # SEO
    meta_description = models.CharField(max_length=160, blank=True)
    meta_keywords = models.CharField(max_length=200, blank=True)
    
    # Settings
    is_active = models.BooleanField(default=True, help_text="Only one record should be active")
    show_on_homepage = models.BooleanField(default=True)
    show_stats = models.BooleanField(default=True, help_text="Show statistics on homepage")
    
    # Management
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "University Information"
        verbose_name_plural = "University Information"
        ordering = ['-is_active', '-updated_at']
    
    def __str__(self):
        return f"{self.name} - {'Active' if self.is_active else 'Inactive'}"
    
    def get_features_list(self):
        """Get list of key features"""
        return [feature.strip() for feature in self.key_features.splitlines() if feature.strip()]
    
    def get_accreditations_list(self):
        """Get list of accreditations"""
        return [acc.strip() for acc in self.accreditations.splitlines() if acc.strip()]
    
    def get_social_links(self):
        """Get dictionary of social media links"""
        links = {}
        if self.facebook_url:
            links['facebook'] = self.facebook_url
        if self.twitter_url:
            links['twitter'] = self.twitter_url
        if self.linkedin_url:
            links['linkedin'] = self.linkedin_url
        if self.instagram_url:
            links['instagram'] = self.instagram_url
        if self.youtube_url:
            links['youtube'] = self.youtube_url
        return links
    
    def save(self, *args, **kwargs):
        # Ensure only one active instance
        if self.is_active:
            UniversityInfo.objects.filter(is_active=True).exclude(pk=self.pk).update(is_active=False)
        super().save(*args, **kwargs)


class UniversityGallery(models.Model):
    """Gallery images for Galgotias University"""
    CATEGORY_CHOICES = [
        ('campus', 'Campus'),
        ('facilities', 'Facilities'),
        ('labs', 'Laboratories'),
        ('library', 'Library'),
        ('hostel', 'Hostel'),
        ('sports', 'Sports & Recreation'),
        ('events', 'Events'),
        ('classrooms', 'Classrooms'),
        ('auditorium', 'Auditorium'),
        ('infrastructure', 'Infrastructure'),
        ('student_life', 'Student Life'),
        ('other', 'Other'),
    ]
    
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='university/gallery/')
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='campus')
    
    # Display Settings
    is_featured = models.BooleanField(default=False, help_text="Show in homepage slider")
    is_active = models.BooleanField(default=True)
    display_order = models.IntegerField(default=0, help_text="Lower numbers appear first")
    
    # Additional Info
    photographer = models.CharField(max_length=100, blank=True)
    photo_date = models.DateField(null=True, blank=True, help_text="When photo was taken")
    
    # Management
    uploaded_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "University Gallery Image"
        verbose_name_plural = "University Gallery Images"
        ordering = ['category', 'display_order', '-created_at']
    
    def __str__(self):
        return f"{self.title} ({self.get_category_display()})"
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        
        # Resize image if too large
        if self.image:
            img_path = self.image.path
            if os.path.exists(img_path):
                with Image.open(img_path) as img:
                    # Resize if larger than 1920x1080
                    if img.height > 1080 or img.width > 1920:
                        img.thumbnail((1920, 1080), Image.Resampling.LANCZOS)
                        img.save(img_path, optimize=True, quality=85)


class FAQCategory(models.Model):
    """FAQ categories for organization"""
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True, blank=True)
    description = models.TextField(blank=True)
    icon = models.CharField(max_length=50, default='fas fa-question-circle', help_text='FontAwesome icon class')
    display_order = models.IntegerField(default=0, help_text='Lower numbers appear first')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'FAQ Category'
        verbose_name_plural = 'FAQ Categories'
        ordering = ['display_order', 'name']
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class FAQ(models.Model):
    """Frequently Asked Questions with AI-powered answers"""
    PRIORITY_CHOICES = [
        ('low', 'Low Priority'),
        ('medium', 'Medium Priority'),
        ('high', 'High Priority'),
        ('critical', 'Critical/Important'),
    ]
    
    category = models.ForeignKey(FAQCategory, on_delete=models.CASCADE, related_name='faqs', null=True, blank=True)
    question = models.TextField(help_text='The FAQ question')
    answer = models.TextField(help_text='The FAQ answer')
    
    # AI Enhancement
    ai_enhanced = models.BooleanField(default=False, help_text='Was this answer enhanced by AI?')
    ai_response = models.TextField(blank=True, help_text='AI-generated response (if applicable)')
    
    # Metadata
    priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES, default='medium')
    views = models.PositiveIntegerField(default=0, help_text='Number of times viewed')
    helpful_count = models.PositiveIntegerField(default=0, help_text='Number of helpful votes')
    not_helpful_count = models.PositiveIntegerField(default=0, help_text='Number of not helpful votes')
    
    # Display Settings
    is_published = models.BooleanField(default=True, help_text='Show on FAQ page')
    is_featured = models.BooleanField(default=False, help_text='Show in featured FAQs')
    display_order = models.IntegerField(default=0, help_text='Lower numbers appear first')
    
    # Tags & Keywords
    tags = models.CharField(max_length=200, blank=True, help_text='Comma-separated tags for search')
    keywords = models.TextField(blank=True, help_text='Keywords for AI matching')
    
    # Management
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='created_faqs')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'FAQ'
        verbose_name_plural = 'FAQs'
        ordering = ['-priority', 'display_order', '-created_at']
        indexes = [
            models.Index(fields=['is_published', '-created_at']),
            models.Index(fields=['category', 'is_published']),
        ]
    
    def __str__(self):
        return self.question[:100]
    
    def increment_views(self):
        """Increment view count"""
        self.views += 1
        self.save(update_fields=['views'])
    
    def mark_helpful(self):
        """Mark as helpful"""
        self.helpful_count += 1
        self.save(update_fields=['helpful_count'])
    
    def mark_not_helpful(self):
        """Mark as not helpful"""
        self.not_helpful_count += 1
        self.save(update_fields=['not_helpful_count'])
    
    def get_tags_list(self):
        """Get list of tags"""
        return [tag.strip() for tag in self.tags.split(',') if tag.strip()]
    
    @property
    def helpfulness_ratio(self):
        """Calculate helpfulness ratio"""
        total = self.helpful_count + self.not_helpful_count
        if total == 0:
            return 0
        return (self.helpful_count / total) * 100


class AIConversation(models.Model):
    """Store AI conversations for FAQ assistance"""
    session_id = models.CharField(max_length=100, db_index=True)
    user_question = models.TextField()
    ai_response = models.TextField()
    matched_faq = models.ForeignKey(FAQ, on_delete=models.SET_NULL, null=True, blank=True, related_name='conversations')
    
    # Feedback
    was_helpful = models.BooleanField(null=True, blank=True)
    feedback_text = models.TextField(blank=True)
    
    # Metadata
    response_time = models.FloatField(default=0, help_text='Response time in seconds')
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'AI Conversation'
        verbose_name_plural = 'AI Conversations'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['session_id', '-created_at']),
        ]
    
    def __str__(self):
        return f"{self.user_question[:50]}... ({self.created_at.strftime('%Y-%m-%d %H:%M')})"


# =============================================================================
# GUIDELINES MODELS
# =============================================================================

class GuidelineCategory(models.Model):
    """Categories for organizing guidelines"""
    ICON_CHOICES = [
        ('fas fa-file-alt', 'Document'),
        ('fas fa-book', 'Book'),
        ('fas fa-list-ol', 'List'),
        ('fas fa-check-circle', 'Check Circle'),
        ('fas fa-info-circle', 'Info Circle'),
        ('fas fa-clipboard-check', 'Clipboard Check'),
        ('fas fa-tasks', 'Tasks'),
        ('fas fa-file-pdf', 'PDF File'),
        ('fas fa-code', 'Code'),
        ('fas fa-image', 'Image'),
    ]
    
    title = models.CharField(max_length=200, help_text='Category name')
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    description = models.TextField(blank=True, help_text='Brief description of this category')
    icon = models.CharField(max_length=50, choices=ICON_CHOICES, default='fas fa-file-alt')
    color = models.CharField(max_length=7, default='#667eea', help_text='Hex color code for category badge')
    display_order = models.IntegerField(default=0, help_text='Lower numbers appear first')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Guideline Category'
        verbose_name_plural = 'Guideline Categories'
        ordering = ['display_order', 'title']
    
    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)


class Guideline(models.Model):
    """Individual guidelines with rich content"""
    CONTENT_TYPE_CHOICES = [
        ('text', 'Text Content'),
        ('checklist', 'Checklist'),
        ('steps', 'Step-by-Step Guide'),
        ('tips', 'Tips & Best Practices'),
        ('requirements', 'Requirements'),
        ('table', 'Table Data'),
    ]
    
    category = models.ForeignKey(GuidelineCategory, on_delete=models.CASCADE, related_name='guidelines', null=True, blank=True)
    title = models.CharField(max_length=300, help_text='Guideline title')
    slug = models.SlugField(max_length=300, unique=True, blank=True)
    
    # Content
    short_description = models.TextField(help_text='Brief summary (1-2 sentences)', max_length=500)
    content = models.TextField(help_text='Main guideline content (supports HTML)')
    content_type = models.CharField(max_length=20, choices=CONTENT_TYPE_CHOICES, default='text')
    
    # Table Data
    table_data = models.JSONField(blank=True, null=True, help_text='Table data in JSON format')
    table_file = models.FileField(upload_to='guidelines/tables/', blank=True, null=True, help_text='Excel or CSV file to import as table')
    table_title = models.CharField(max_length=200, blank=True, help_text='Title for the table')
    table_has_header = models.BooleanField(default=True, help_text='First row contains headers')
    
    # Additional resources
    additional_info = models.TextField(blank=True, help_text='Extra information, notes, or warnings')
    downloadable_file = models.FileField(upload_to='guidelines/files/', blank=True, null=True, help_text='PDF, DOCX, or other file')
    external_link = models.URLField(blank=True, help_text='External resource URL')
    video_url = models.URLField(blank=True, help_text='YouTube or Vimeo URL')
    
    # Display settings
    is_important = models.BooleanField(default=False, help_text='Highlight as important')
    is_published = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False, help_text='Show in featured section')
    display_order = models.IntegerField(default=0)
    
    # Metadata
    views = models.PositiveIntegerField(default=0)
    helpful_count = models.PositiveIntegerField(default=0)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='created_guidelines')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Guideline'
        verbose_name_plural = 'Guidelines'
        ordering = ['-is_featured', '-is_important', 'display_order', 'title']
    
    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)
    
    def increment_views(self):
        """Increment view count"""
        self.views += 1
        self.save(update_fields=['views'])
    
    def mark_helpful(self):
        """Mark as helpful"""
        self.helpful_count += 1
        self.save(update_fields=['helpful_count'])


class GuidelineChecklist(models.Model):
    """Checklist items for guidelines"""
    guideline = models.ForeignKey(Guideline, on_delete=models.CASCADE, related_name='checklist_items')
    item_text = models.CharField(max_length=500)
    description = models.TextField(blank=True)
    is_required = models.BooleanField(default=False, help_text='Mark as required/mandatory')
    display_order = models.IntegerField(default=0)
    
    class Meta:
        verbose_name = 'Checklist Item'
        verbose_name_plural = 'Checklist Items'
        ordering = ['display_order', 'id']
    
    def __str__(self):
        return f"{self.guideline.title} - {self.item_text[:50]}"


# =============================================================================
# AWARDS MODELS
# =============================================================================

class AwardCategory(models.Model):
    """Award categories"""
    CATEGORY_TYPE_CHOICES = [
        ('paper', 'Best Paper Awards'),
        ('presentation', 'Best Presentation Awards'),
        ('poster', 'Best Poster Awards'),
        ('student', 'Student Awards'),
        ('research', 'Research Excellence Awards'),
        ('innovation', 'Innovation Awards'),
        ('service', 'Service Awards'),
        ('special', 'Special Recognition'),
    ]
    
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    category_type = models.CharField(max_length=20, choices=CATEGORY_TYPE_CHOICES, default='paper')
    description = models.TextField(help_text='Description of this award category')
    icon = models.CharField(max_length=50, default='fas fa-trophy')
    color = models.CharField(max_length=7, default='#ffd700', help_text='Hex color for badge/icon')
    prize_details = models.TextField(blank=True, help_text='Prize money, certificate, etc.')
    eligibility = models.TextField(blank=True, help_text='Who can apply for this award')
    
    # Display settings
    display_order = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    show_on_homepage = models.BooleanField(default=False)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Award Category'
        verbose_name_plural = 'Award Categories'
        ordering = ['display_order', 'name']
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Award(models.Model):
    """Individual awards and winners"""
    STATUS_CHOICES = [
        ('upcoming', 'Upcoming - Not Yet Awarded'),
        ('open', 'Open for Nominations'),
        ('closed', 'Nominations Closed'),
        ('announced', 'Winner Announced'),
    ]
    
    category = models.ForeignKey(AwardCategory, on_delete=models.CASCADE, related_name='awards')
    title = models.CharField(max_length=300, help_text='Award title/name')
    slug = models.SlugField(max_length=300, unique=True, blank=True)
    description = models.TextField(help_text='Award description and criteria')
    
    # Winner information (if announced)
    winner_name = models.CharField(max_length=300, blank=True)
    winner_affiliation = models.CharField(max_length=300, blank=True, help_text='University/Organization')
    winner_photo = models.ImageField(upload_to='awards/winners/', blank=True, null=True)
    winner_bio = models.TextField(blank=True)
    winning_work_title = models.CharField(max_length=500, blank=True, help_text='Paper/Project title')
    winning_work_description = models.TextField(blank=True)
    
    # Award details
    prize_amount = models.CharField(max_length=100, blank=True, help_text='e.g., $500, Certificate + Trophy')
    sponsored_by = models.CharField(max_length=200, blank=True, help_text='Sponsor name')
    
    # Timeline
    nomination_start = models.DateField(null=True, blank=True)
    nomination_end = models.DateField(null=True, blank=True)
    announcement_date = models.DateField(null=True, blank=True)
    
    # Status
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='upcoming')
    is_featured = models.BooleanField(default=False)
    
    # Display
    display_order = models.IntegerField(default=0)
    year = models.IntegerField(default=2026, help_text='Conference year')
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Award'
        verbose_name_plural = 'Awards'
        ordering = ['-year', '-is_featured', 'display_order', 'title']
    
    def __str__(self):
        return f"{self.title} ({self.year})"
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(f"{self.title}-{self.year}")
        super().save(*args, **kwargs)
    
    @property
    def is_nomination_open(self):
        """Check if nomination period is active"""
        from django.utils import timezone
        if not self.nomination_start or not self.nomination_end:
            return False
        today = timezone.now().date()
        return self.nomination_start <= today <= self.nomination_end


class AwardCriteria(models.Model):
    """Evaluation criteria for awards"""
    award = models.ForeignKey(Award, on_delete=models.CASCADE, related_name='criteria')
    criterion_name = models.CharField(max_length=200, help_text='e.g., Originality, Impact, Presentation')
    description = models.TextField(blank=True)
    weight_percentage = models.IntegerField(default=0, help_text='Weight in evaluation (0-100)')
    display_order = models.IntegerField(default=0)
    
    class Meta:
        verbose_name = 'Award Criterion'
        verbose_name_plural = 'Award Criteria'
        ordering = ['display_order', 'criterion_name']
    
    def __str__(self):
        return f"{self.award.title} - {self.criterion_name}"


class PastWinner(models.Model):
    """Past award winners from previous conferences"""
    award_name = models.CharField(max_length=300)
    year = models.IntegerField()
    winner_name = models.CharField(max_length=300)
    winner_affiliation = models.CharField(max_length=300, blank=True)
    winner_photo = models.ImageField(upload_to='awards/past_winners/', blank=True, null=True)
    work_title = models.CharField(max_length=500, blank=True)
    work_description = models.TextField(blank=True)
    
    display_order = models.IntegerField(default=0)
    is_featured = models.BooleanField(default=False)
    
    class Meta:
        verbose_name = 'Past Winner'
        verbose_name_plural = 'Past Winners'
        ordering = ['-year', 'display_order']
    
    def __str__(self):
        return f"{self.winner_name} - {self.award_name} ({self.year})"


# =============================================================================
# SITE SETTINGS - Logos, Images, Hero Slider Configuration
# =============================================================================

class SiteSettings(models.Model):
    """Global site settings for logos, images, and configurations"""
    
    # Site Information
    site_name = models.CharField(max_length=200, default='ICCCA 2026')
    site_tagline = models.CharField(max_length=500, blank=True, help_text='Tagline shown in header/footer')
    
    # Logos
    main_logo = models.ImageField(upload_to='site/logos/', blank=True, null=True, help_text='Main logo (used in header)')
    footer_logo = models.ImageField(upload_to='site/logos/', blank=True, null=True, help_text='Footer logo (can be different from main)')
    favicon = models.ImageField(upload_to='site/logos/', blank=True, null=True, help_text='Browser favicon (16x16 or 32x32 px)')
    
    # Contact Information
    contact_email = models.EmailField(blank=True)
    contact_phone = models.CharField(max_length=50, blank=True)
    contact_address = models.TextField(blank=True)
    
    # Social Media Links
    facebook_url = models.URLField(blank=True)
    twitter_url = models.URLField(blank=True)
    linkedin_url = models.URLField(blank=True)
    instagram_url = models.URLField(blank=True)
    youtube_url = models.URLField(blank=True)
    
    # Theme Colors
    primary_color = models.CharField(max_length=7, default='#a0352f', help_text='Hex color code (e.g., #a0352f)')
    secondary_color = models.CharField(max_length=7, default='#e56d2d', help_text='Hex color code (e.g., #e56d2d)')
    
    # Submit Paper Button
    submit_paper_url = models.URLField(blank=True, default='#submit-paper', help_text='URL for Submit Paper button (default: #submit-paper)')
    submit_paper_text = models.CharField(max_length=50, default='Submit Paper', help_text='Text for Submit Paper button')
    
    # Meta
    updated_at = models.DateTimeField(auto_now=True)
    updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    
    class Meta:
        verbose_name = 'Website Control - Site Settings'
        verbose_name_plural = 'Website Control - Site Settings'
    
    def __str__(self):
        return f"Site Settings - {self.site_name}"
    
    def save(self, *args, **kwargs):
        # Ensure only one instance exists
        if not self.pk and SiteSettings.objects.exists():
            # Update existing instance instead of creating new
            existing = SiteSettings.objects.first()
            self.pk = existing.pk
        super().save(*args, **kwargs)
    
    @classmethod
    def get_settings(cls):
        """Get or create site settings"""
        settings, created = cls.objects.get_or_create(pk=1)
        return settings


class HeroSlide(models.Model):
    """Hero slider slides with images or videos"""
    
    SLIDE_TYPE_CHOICES = [
        ('image', 'Image Slide'),
        ('video', 'Video Slide'),
    ]
    
    title = models.CharField(max_length=200, blank=True, help_text='Slide title (optional overlay text)')
    subtitle = models.CharField(max_length=500, blank=True, help_text='Subtitle or description')
    slide_type = models.CharField(max_length=10, choices=SLIDE_TYPE_CHOICES, default='image')
    
    # Image Slide
    image = models.ImageField(upload_to='hero/slides/', blank=True, null=True, help_text='Slide background image')
    
    # Video Slide
    video_file = models.FileField(upload_to='hero/videos/', blank=True, null=True, help_text='Upload video file (MP4, WebM)')
    video_url = models.URLField(blank=True, help_text='Or use YouTube/Vimeo URL')
    video_thumbnail = models.ImageField(upload_to='hero/thumbnails/', blank=True, null=True, help_text='Video thumbnail/poster image')
    
    # Call to Action
    cta_text = models.CharField(max_length=100, blank=True, help_text='Button text (e.g., "Register Now")')
    cta_url = models.CharField(max_length=500, blank=True, help_text='Button link URL')
    cta_style = models.CharField(max_length=20, default='primary', choices=[
        ('primary', 'Primary Button'),
        ('secondary', 'Secondary Button'),
        ('outline', 'Outline Button'),
    ])
    
    # Display Settings
    display_order = models.IntegerField(default=0, help_text='Lower numbers appear first')
    is_active = models.BooleanField(default=True)
    
    # Text Overlay Settings
    text_position = models.CharField(max_length=20, default='center', choices=[
        ('left', 'Left'),
        ('center', 'Center'),
        ('right', 'Right'),
    ])
    text_color = models.CharField(max_length=7, default='#ffffff', help_text='Text overlay color (hex)')
    show_overlay = models.BooleanField(default=True, help_text='Show dark overlay for better text readability')
    
    # Meta
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Website Control - Hero Slider'
        verbose_name_plural = 'Website Control - Hero Sliders'
        ordering = ['display_order', '-created_at']
    
    def __str__(self):
        return f"{self.title} ({self.get_slide_type_display()})"


class SliderSettings(models.Model):
    """Global slider configuration and controls"""
    
    # Slider Controls
    autoplay = models.BooleanField(default=True, help_text='Auto-advance slides')
    autoplay_speed = models.IntegerField(default=5000, help_text='Milliseconds between slides (e.g., 5000 = 5 seconds)')
    transition_speed = models.IntegerField(default=1000, help_text='Transition duration in milliseconds (e.g., 1000 = 1 second)')
    
    transition_effect = models.CharField(max_length=20, default='fade', choices=[
        ('fade', 'Fade'),
        ('slide', 'Slide'),
        ('zoom', 'Zoom'),
        ('slide-fade', 'Slide + Fade'),
    ])
    
    # Navigation
    show_arrows = models.BooleanField(default=True, help_text='Show prev/next arrows')
    show_dots = models.BooleanField(default=True, help_text='Show navigation dots')
    pause_on_hover = models.BooleanField(default=True, help_text='Pause autoplay when hovering')
    
    # Mobile Settings
    autoplay_mobile = models.BooleanField(default=True, help_text='Enable autoplay on mobile devices')
    show_arrows_mobile = models.BooleanField(default=False, help_text='Show arrows on mobile')
    
    # Hero Slider Height
    slider_height_desktop = models.IntegerField(default=700, help_text='Slider height on desktop (pixels)')
    slider_height_mobile = models.IntegerField(default=500, help_text='Slider height on mobile (pixels)')
    
    # Performance
    lazy_load = models.BooleanField(default=True, help_text='Lazy load images for better performance')
    preload_slides = models.IntegerField(default=2, help_text='Number of slides to preload (1-5)')
    
    # Meta
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Website Control - Slider Settings'
        verbose_name_plural = 'Website Control - Slider Settings'
    
    def __str__(self):
        return f"Slider Settings (Speed: {self.autoplay_speed}ms)"
    
    def save(self, *args, **kwargs):
        # Ensure only one instance exists
        if not self.pk and SliderSettings.objects.exists():
            existing = SliderSettings.objects.first()
            self.pk = existing.pk
        super().save(*args, **kwargs)
    
    @classmethod
    def get_settings(cls):
        """Get or create slider settings"""
        settings, created = cls.objects.get_or_create(pk=1)
        return settings


# =============================================================================
# SIGNALS - Auto-parse tables when Guideline is saved
# =============================================================================

from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_save, sender=Guideline)
def auto_parse_guideline_table(sender, instance, created, **kwargs):
    """Automatically parse table file when a Guideline is saved"""
    # Only parse if:
    # 1. Table file exists
    # 2. Content type is 'table'
    # 3. Table data is not already populated (to avoid infinite loop)
    # 4. This is not already a recursive save
    
    if hasattr(instance, '_parsing_table'):
        # Prevent infinite recursion
        return
    
    if instance.table_file and instance.content_type == 'table' and not instance.table_data:
        try:
            from conference.utils.table_parser import parse_table_file
            import os
            
            # Mark that we're parsing to prevent recursion
            instance._parsing_table = True
            
            file_path = instance.table_file.path
            if os.path.exists(file_path):
                table_data = parse_table_file(file_path, instance.table_has_header)
                # Update only table_data field to avoid triggering full save
                Guideline.objects.filter(pk=instance.pk).update(table_data=table_data)
                # Update the instance in memory
                instance.table_data = table_data
                print(f"✅ Auto-parsed table for '{instance.title}': {table_data['total_rows']} rows × {table_data['total_columns']} columns")
        except Exception as e:
            print(f"❌ Error auto-parsing table for '{instance.title}': {str(e)}")
            import traceback
            traceback.print_exc()
        finally:
            # Clean up the flag
            if hasattr(instance, '_parsing_table'):
                delattr(instance, '_parsing_table')