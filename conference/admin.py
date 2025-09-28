from django.contrib import admin
from .models import (
    CommitteeMember, ConferenceTrack, TouristAttraction, 
    ImportantDate, Slider, ConferenceSettings, Sponsor
)

@admin.register(CommitteeMember)
class CommitteeMemberAdmin(admin.ModelAdmin):
    list_display = ['name', 'title', 'organization', 'order']
    list_editable = ['order']
    list_filter = ['organization']
    search_fields = ['name', 'title', 'organization']

@admin.register(ConferenceTrack)
class ConferenceTrackAdmin(admin.ModelAdmin):
    list_display = ['track_number', 'title', 'track_type', 'track_chair']
    list_filter = ['track_type']
    search_fields = ['title', 'description']
    ordering = ['track_number']

@admin.register(TouristAttraction)
class TouristAttractionAdmin(admin.ModelAdmin):
    list_display = ['name', 'order']
    list_editable = ['order']
    search_fields = ['name', 'description']

@admin.register(ImportantDate)
class ImportantDateAdmin(admin.ModelAdmin):
    list_display = ['event', 'date', 'order']
    list_editable = ['order']
    date_hierarchy = 'date'

@admin.register(Slider)
class SliderAdmin(admin.ModelAdmin):
    list_display = ['title', 'order', 'is_active']
    list_editable = ['order', 'is_active']
    list_filter = ['is_active']

@admin.register(ConferenceSettings)
class ConferenceSettingsAdmin(admin.ModelAdmin):
    list_display = ['site_title', 'conference_dates', 'location']

@admin.register(Sponsor)
class SponsorAdmin(admin.ModelAdmin):
    list_display = ['name', 'order']
    list_editable = ['order']
