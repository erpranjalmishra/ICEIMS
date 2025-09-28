from django.db import models
from django.utils.text import slugify

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
