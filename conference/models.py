from django.db import models
from django.utils.text import slugify
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone
from PIL import Image
import os

class CommitteeMember(models.Model):
    name = models.CharField(max_length=200)
    title = models.CharField(max_length=300)
    organization = models.CharField(max_length=300)
    image = models.ImageField(upload_to='committee/', blank=True, null=True)
    order = models.IntegerField(default=0)
    
    class Meta:
        ordering = ['order', 'name']
    
    def __str__(self):
        return f"{self.name} - {self.title}"

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
