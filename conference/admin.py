from django.contrib import admin
from django import forms
from django.utils.html import format_html
from django.urls import path
from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.cache import cache
from .models import (
    HierarchyLevel, CommitteeMember, ConferenceTrack, TouristAttraction, 
    ImportantDate, Slider, ConferenceSettings, Sponsor, UniversityInfo, UniversityGallery,
    FAQCategory, FAQ, AIConversation, GuidelineCategory, Guideline, GuidelineChecklist,
    AwardCategory, Award, AwardCriteria, PastWinner, AwardGallery,
    SiteSettings, HeroSlide, SliderSettings, MarqueeText, ConferenceTopic,
    VisitorCounter, RegistrationCategory, ConferenceRegistration, RegistrationSettings,
    RegistrationFeesTable, DownloadResource, Speaker, LoadingPageSettings,
    AboutPage, AboutObjective, SponsorsPageSettings, PageVisitLog, SitemapLink
)


# Admin Action: Manual Cache Clear
def clear_site_cache(modeladmin, request, queryset):
    """Admin action to manually clear all caches"""
    cache.clear()
    messages.success(request, '🔄 Cache cleared successfully! All changes will now be visible on the website.')
clear_site_cache.short_description = "🔄 Clear website cache (force refresh)"

# Custom Admin Site Configuration
class CustomAdminSite(admin.AdminSite):
    site_header = 'ICEIMS 2026 Administration'
    site_title = 'ICEIMS Admin'
    index_title = 'Conference Management Dashboard'
    
    def login(self, request, extra_context=None):
        """
        Override login to redirect to custom admin dashboard after successful login
        """
        if request.method == 'POST':
            response = super().login(request, extra_context)
            # If login was successful (user is authenticated), redirect to admin dashboard
            if request.user.is_authenticated:
                from django.shortcuts import redirect
                return redirect('conference:admin_dashboard')
            return response
        return super().login(request, extra_context)

# Create custom admin site instance
custom_admin_site = CustomAdminSite(name='custom_admin')

class CommitteeMemberForm(forms.ModelForm):
    """Custom form for CommitteeMember with dynamic hierarchy choices"""
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Dynamically populate hierarchy_level choices from database
        hierarchy_choices = [(level.level_number, f"Level {level.level_number} - {level.level_name}") 
                           for level in HierarchyLevel.objects.filter(is_active=True).order_by('level_number')]
        
        # If no levels exist, provide default choices
        if not hierarchy_choices:
            hierarchy_choices = [(i, f"Level {i}") for i in range(1, 9)]
        
        self.fields['hierarchy_level'] = forms.ChoiceField(
            choices=hierarchy_choices,
            initial=8,
            help_text="Select the hierarchical level (managed in Hierarchy Levels section)",
            widget=forms.Select(attrs={'class': 'form-control'})
        )
    
    class Meta:
        model = CommitteeMember
        fields = '__all__'

@admin.register(HierarchyLevel)
class HierarchyLevelAdmin(admin.ModelAdmin):
    list_display = ['level_number', 'level_name', 'description', 'is_active', 'member_count']
    list_editable = ['level_name', 'is_active']
    list_filter = ['is_active']
    search_fields = ['level_name', 'description']
    ordering = ['level_number']
    fields = ['level_number', 'level_name', 'description', 'is_active']
    
    def member_count(self, obj):
        """Show count of committee members in this level"""
        count = CommitteeMember.objects.filter(hierarchy_level=obj.level_number, is_active=True).count()
        return f"{count} member{'s' if count != 1 else ''}"
    member_count.short_description = 'Active Members'
    
    def has_delete_permission(self, request, obj=None):
        # Allow deletion only if no members are assigned to this level
        if obj:
            member_count = CommitteeMember.objects.filter(hierarchy_level=obj.level_number).count()
            return member_count == 0
        return True
    
    def get_readonly_fields(self, request, obj=None):
        # Make level_number readonly after creation to prevent conflicts
        if obj:
            return ['level_number']
        return []

@admin.register(CommitteeMember)
class CommitteeMemberAdmin(admin.ModelAdmin):
    form = CommitteeMemberForm  # Use custom form with dynamic hierarchy choices
    list_display = ['name', 'title', 'organization', 'get_level_name_display', 'hierarchy_level', 'order', 'enable_bio_page', 'page_views', 'is_active']
    list_editable = ['order', 'enable_bio_page', 'is_active']
    list_filter = ['organization', 'hierarchy_level', 'role', 'enable_bio_page', 'is_active']
    search_fields = ['name', 'title', 'organization', 'bio', 'detailed_bio']
    ordering = ['hierarchy_level', 'order']
    readonly_fields = ['slug', 'page_views', 'last_viewed', 'view_bio_page_link']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'slug', 'title', 'organization', 'image')
        }),
        ('Hierarchy & Role', {
            'fields': ('hierarchy_level', 'role', 'order'),
            'description': 'Assign a hierarchy level. You can add more levels in the "Hierarchy Levels" section.'
        }),
        ('Biography', {
            'fields': ('bio', 'detailed_bio'),
            'description': 'Bio shows on committee page. Detailed bio shows on dedicated bio page.'
        }),
        ('Extended Information', {
            'fields': ('research_interests', 'education', 'publications', 'awards'),
            'classes': ('collapse',)
        }),
        ('Contact Information', {
            'fields': ('email', 'phone'),
            'classes': ('collapse',)
        }),
        ('Social Media Links', {
            'fields': ('website', 'linkedin', 'twitter', 'google_scholar', 'orcid', 'researchgate'),
            'classes': ('collapse',)
        }),
        ('Page Settings', {
            'fields': ('enable_bio_page', 'view_bio_page_link', 'is_active'),
        }),
        ('Analytics', {
            'fields': ('page_views', 'last_viewed'),
            'classes': ('collapse',)
        }),
    )
    
    def get_level_name_display(self, obj):
        """Show the hierarchy level name instead of just the number"""
        return obj.get_hierarchy_level_name()
    get_level_name_display.short_description = 'Level Name'
    get_level_name_display.admin_order_field = 'hierarchy_level'
    
    def view_bio_page_link(self, obj):
        """Link to view the bio page"""
        if obj.pk and obj.enable_bio_page:
            from django.urls import reverse
            url = reverse('conference:committee_bio', kwargs={'slug': obj.slug})
            return format_html('<a href="{}" target="_blank" class="button">View Bio Page</a>', url)
        return "Save to generate bio page"
    view_bio_page_link.short_description = 'Bio Page'

@admin.register(ConferenceTrack)
class ConferenceTrackAdmin(admin.ModelAdmin):
    list_display = ['track_number', 'title_with_color', 'track_type', 'track_chair', 'topic_count', 'is_active_display']
    list_editable = ['track_type']
    list_filter = ['track_type', 'is_active', 'created_at']
    search_fields = ['title', 'description', 'track_chair']
    ordering = ['display_order', 'track_number']
    readonly_fields = ['created_at', 'updated_at', 'topic_preview']
    actions = ['make_active', 'make_inactive', 'duplicate_track']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('track_number', 'title', 'track_type')
        }),
        ('Track Details', {
            'fields': ('description', 'track_chair', 'image'),
            'description': 'Add track topics/areas - one per line in the description field.'
        }),
        ('Display Settings', {
            'fields': ('is_active', 'display_order', 'color'),
            'classes': ('collapse',)
        }),
        ('Additional Information', {
            'fields': ('topic_preview', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def title_with_color(self, obj):
        """Display title with color indicator"""
        return format_html(
            '<span style="border-left: 4px solid {}; padding-left: 8px;">{}</span>',
            obj.color,
            obj.title[:50] + ('...' if len(obj.title) > 50 else '')
        )
    title_with_color.short_description = 'Title'
    title_with_color.admin_order_field = 'title'
    
    def topic_count(self, obj):
        """Count the number of topics in the track"""
        count = obj.topic_count()
        return format_html(
            '<span class="field-topic_count">{} topic{}</span>',
            count,
            's' if count != 1 else ''
        )
    topic_count.short_description = 'Topics'
    
    def is_active_display(self, obj):
        """Display active status with icon"""
        if obj.is_active:
            return format_html('<span style="color: green;">✓ Active</span>')
        return format_html('<span style="color: #ccc;">✗ Inactive</span>')
    is_active_display.short_description = 'Status'
    is_active_display.admin_order_field = 'is_active'
    
    def topic_preview(self, obj):
        """Show preview of topics"""
        topics = obj.get_topics_list()
        if topics:
            preview = topics[:5]  # Show first 5 topics
            result = "<ul>"
            for topic in preview:
                result += f"<li>{topic}</li>"
            if len(topics) > 5:
                result += f"<li><em>... and {len(topics) - 5} more</em></li>"
            result += "</ul>"
            return format_html(result)
        return "No topics added yet"
    topic_preview.short_description = 'Topics Preview'
    
    # Bulk actions
    def make_active(self, request, queryset):
        """Activate selected tracks"""
        updated = queryset.update(is_active=True)
        self.message_user(request, f'{updated} track(s) were successfully activated.', messages.SUCCESS)
    make_active.short_description = 'Activate selected tracks'
    
    def make_inactive(self, request, queryset):
        """Deactivate selected tracks"""
        updated = queryset.update(is_active=False)
        self.message_user(request, f'{updated} track(s) were successfully deactivated.', messages.SUCCESS)
    make_inactive.short_description = 'Deactivate selected tracks'
    
    def duplicate_track(self, request, queryset):
        """Duplicate selected tracks"""
        count = 0
        for track in queryset:
            # Get the highest track number
            max_track_num = ConferenceTrack.objects.all().order_by('-track_number').first()
            new_track_num = (max_track_num.track_number + 1) if max_track_num else 1
            
            # Create duplicate
            track.pk = None
            track.track_number = new_track_num
            track.title = f"{track.title} (Copy)"
            track.is_active = False  # Set copies as inactive by default
            track.save()
            count += 1
        
        self.message_user(request, f'{count} track(s) were successfully duplicated.', messages.SUCCESS)
    duplicate_track.short_description = 'Duplicate selected tracks'
    
    class Media:
        css = {
            'all': ('admin/css/custom_admin.css',)
        }
        js = ('admin/js/track_admin.js',)

@admin.register(TouristAttraction)
class TouristAttractionAdmin(admin.ModelAdmin):
    list_display = ['name', 'order']
    list_editable = ['order']
    search_fields = ['name', 'description']

@admin.register(ImportantDate)
class ImportantDateAdmin(admin.ModelAdmin):
    list_display = ['event', 'date', 'order', 'has_link']
    list_editable = ['order']
    date_hierarchy = 'date'
    fieldsets = (
        ('Event Details', {
            'fields': ('event', 'date', 'description', 'order')
        }),
        ('Link Settings', {
            'fields': ('link_url', 'link_text', 'open_in_new_tab'),
            'description': 'Add an optional link to this event (e.g., registration page, submission portal)'
        }),
    )
    
    def has_link(self, obj):
        return bool(obj.link_url)
    has_link.boolean = True
    has_link.short_description = 'Has Link'

@admin.register(Slider)
class SliderAdmin(admin.ModelAdmin):
    list_display = ['title', 'order', 'is_active']
    list_editable = ['order', 'is_active']
    list_filter = ['is_active']
    actions = [clear_site_cache]

@admin.register(ConferenceSettings)
class ConferenceSettingsAdmin(admin.ModelAdmin):
    list_display = ['site_title', 'conference_dates', 'location']
    actions = [clear_site_cache]

@admin.register(Sponsor)
class SponsorAdmin(admin.ModelAdmin):
    list_display = ['name', 'order']
    list_editable = ['order']
    actions = [clear_site_cache]

@admin.register(UniversityInfo)
class UniversityInfoAdmin(admin.ModelAdmin):
    list_display = ['name', 'is_active', 'show_on_homepage', 'show_stats', 'updated_at']
    list_filter = ['is_active', 'show_on_homepage', 'show_stats']
    list_editable = ['is_active', 'show_on_homepage', 'show_stats']
    search_fields = ['name', 'about_text', 'full_description']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'tagline', 'established_year')
        }),
        ('Content', {
            'fields': ('about_text', 'full_description')
        }),
        ('Statistics', {
            'fields': (
                'student_count', 'school_count', 'program_count', 
                'faculty_count', 'campus_area'
            )
        }),
        ('Location', {
            'fields': ('address', 'city', 'state', 'country', 'pincode')
        }),
        ('Contact Information', {
            'fields': ('phone', 'email', 'website')
        }),
        ('Social Media', {
            'fields': (
                'facebook_url', 'twitter_url', 'linkedin_url', 
                'instagram_url', 'youtube_url'
            ),
            'classes': ('collapse',)
        }),
        ('Features & Highlights', {
            'fields': ('key_features', 'accreditations')
        }),
        ('SEO', {
            'fields': ('meta_description', 'meta_keywords'),
            'classes': ('collapse',)
        }),
        ('Display Settings', {
            'fields': ('is_active', 'show_on_homepage', 'show_stats')
        }),
    )

@admin.register(UniversityGallery)
class UniversityGalleryAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'is_featured', 'is_active', 'display_order', 'created_at']
    list_filter = ['category', 'is_featured', 'is_active']
    list_editable = ['is_featured', 'is_active', 'display_order']
    search_fields = ['title', 'description']
    readonly_fields = ['uploaded_by', 'created_at', 'updated_at']
    
    fieldsets = (
        ('Image Information', {
            'fields': ('title', 'description', 'image', 'category')
        }),
        ('Display Settings', {
            'fields': ('is_featured', 'is_active', 'display_order')
        }),
        ('Additional Info', {
            'fields': ('photographer', 'photo_date'),
            'classes': ('collapse',)
        }),
        ('System Info', {
            'fields': ('uploaded_by', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def save_model(self, request, obj, form, change):
        if not change:  # If creating new object
            obj.uploaded_by = request.user
        super().save_model(request, obj, form, change)

# Register all models with both default and custom admin sites
custom_admin_site.register(HierarchyLevel, HierarchyLevelAdmin)
custom_admin_site.register(CommitteeMember, CommitteeMemberAdmin)
custom_admin_site.register(ConferenceTrack, ConferenceTrackAdmin)
custom_admin_site.register(TouristAttraction, TouristAttractionAdmin)
custom_admin_site.register(ImportantDate, ImportantDateAdmin)
custom_admin_site.register(Slider, SliderAdmin)
custom_admin_site.register(ConferenceSettings, ConferenceSettingsAdmin)
custom_admin_site.register(Sponsor, SponsorAdmin)
custom_admin_site.register(UniversityInfo, UniversityInfoAdmin)
custom_admin_site.register(UniversityGallery, UniversityGalleryAdmin)


# FAQ Category Admin
@admin.register(FAQCategory, site=custom_admin_site)
class FAQCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'icon', 'display_order', 'faq_count', 'is_active', 'created_at')
    list_filter = ('is_active', 'created_at')
    search_fields = ('name', 'description')
    prepopulated_fields = {'slug': ('name',)}
    ordering = ('display_order', 'name')
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'slug', 'description', 'icon')
        }),
        ('Display Settings', {
            'fields': ('display_order', 'is_active')
        }),
    )
    
    def faq_count(self, obj):
        """Count FAQs in this category"""
        count = obj.faqs.filter(is_published=True).count()
        return format_html('<span style="font-weight: bold; color: #007bff;">{}</span>', count)
    faq_count.short_description = 'Published FAQs'

# Also register with default admin
admin.site.register(FAQCategory, FAQCategoryAdmin)


# FAQ Admin
@admin.register(FAQ, site=custom_admin_site)
class FAQAdmin(admin.ModelAdmin):
    list_display = ('question_preview', 'category', 'priority', 'views', 'helpfulness', 'is_published', 'is_featured', 'created_at')
    list_filter = ('category', 'priority', 'is_published', 'is_featured', 'ai_enhanced', 'created_at')
    search_fields = ('question', 'answer', 'tags', 'keywords')
    list_editable = ('is_published', 'is_featured', 'priority')
    ordering = ('-priority', 'display_order', '-created_at')
    readonly_fields = ('views', 'helpful_count', 'not_helpful_count', 'helpfulness_ratio', 'created_at', 'updated_at')
    
    fieldsets = (
        ('Question & Answer', {
            'fields': ('category', 'question', 'answer')
        }),
        ('AI Enhancement', {
            'fields': ('ai_enhanced', 'ai_response'),
            'classes': ('collapse',),
            'description': 'AI-generated content for this FAQ'
        }),
        ('Display Settings', {
            'fields': ('priority', 'is_published', 'is_featured', 'display_order')
        }),
        ('Search & Tags', {
            'fields': ('tags', 'keywords'),
            'classes': ('collapse',),
        }),
        ('Statistics', {
            'fields': ('views', 'helpful_count', 'not_helpful_count', 'helpfulness_ratio'),
            'classes': ('collapse',),
        }),
        ('Metadata', {
            'fields': ('created_by', 'created_at', 'updated_at'),
            'classes': ('collapse',),
        }),
    )
    
    def save_model(self, request, obj, form, change):
        """Auto-set created_by"""
        if not change:
            obj.created_by = request.user
        super().save_model(request, obj, form, change)
    
    def question_preview(self, obj):
        """Show preview of question"""
        preview = obj.question[:80] + '...' if len(obj.question) > 80 else obj.question
        return format_html('<strong>{}</strong>', preview)
    question_preview.short_description = 'Question'
    
    def helpfulness(self, obj):
        """Show helpfulness ratio"""
        ratio = obj.helpfulness_ratio
        if ratio >= 75:
            color = '#28a745'  # green
        elif ratio >= 50:
            color = '#ffc107'  # yellow
        else:
            color = '#dc3545'  # red
        
        return format_html(
            '<span style="color: {}; font-weight: bold;">{:.1f}%</span> ({} / {})',
            color, ratio, obj.helpful_count, obj.helpful_count + obj.not_helpful_count
        )
    helpfulness.short_description = 'Helpfulness'

# Also register with default admin
admin.site.register(FAQ, FAQAdmin)


# AI Conversation Admin
@admin.register(AIConversation, site=custom_admin_site)
class AIConversationAdmin(admin.ModelAdmin):
    list_display = ('question_preview', 'session_id', 'matched_faq', 'was_helpful', 'response_time', 'created_at')
    list_filter = ('was_helpful', 'created_at')
    search_fields = ('user_question', 'ai_response', 'session_id')
    readonly_fields = ('session_id', 'user_question', 'ai_response', 'matched_faq', 'response_time', 'ip_address', 'user_agent', 'created_at')
    ordering = ('-created_at',)
    
    fieldsets = (
        ('Conversation', {
            'fields': ('session_id', 'user_question', 'ai_response', 'matched_faq')
        }),
        ('Feedback', {
            'fields': ('was_helpful', 'feedback_text')
        }),
        ('Technical Details', {
            'fields': ('response_time', 'ip_address', 'user_agent', 'created_at'),
            'classes': ('collapse',),
        }),
    )
    
    def question_preview(self, obj):
        """Show preview of user question"""
        preview = obj.user_question[:60] + '...' if len(obj.user_question) > 60 else obj.user_question
        return preview
    question_preview.short_description = 'User Question'
    
    def has_add_permission(self, request):
        """Don't allow manual creation"""
        return False

# Also register with default admin
admin.site.register(AIConversation, AIConversationAdmin)


# =============================================================================
# GUIDELINES ADMIN
# =============================================================================

@admin.register(GuidelineCategory, site=custom_admin_site)
class GuidelineCategoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'icon_preview', 'color_preview', 'guidelines_count', 'display_order', 'is_active', 'created_at')
    list_filter = ('is_active', 'created_at')
    search_fields = ('title', 'description')
    prepopulated_fields = {'slug': ('title',)}
    ordering = ('display_order', 'title')
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'slug', 'description')
        }),
        ('Appearance', {
            'fields': ('icon', 'color')
        }),
        ('Settings', {
            'fields': ('display_order', 'is_active')
        }),
    )
    
    def icon_preview(self, obj):
        """Show icon preview"""
        return format_html('<i class="{}" style="font-size: 1.5rem; color: {};"></i>', obj.icon, obj.color)
    icon_preview.short_description = 'Icon'
    
    def color_preview(self, obj):
        """Show color preview"""
        return format_html('<span style="background: {}; padding: 5px 15px; border-radius: 5px; color: white;">{}</span>', obj.color, obj.color)
    color_preview.short_description = 'Color'
    
    def guidelines_count(self, obj):
        """Count guidelines in category"""
        count = obj.guidelines.filter(is_published=True).count()
        return format_html('<span style="font-weight: bold; color: #007bff;">{}</span>', count)
    guidelines_count.short_description = 'Published Guidelines'

# Also register with default admin
admin.site.register(GuidelineCategory, GuidelineCategoryAdmin)


class GuidelineChecklistInline(admin.TabularInline):
    model = GuidelineChecklist
    extra = 1
    fields = ('item_text', 'description', 'is_required', 'display_order')
    ordering = ('display_order',)


class GuidelineAdmin(admin.ModelAdmin):
    list_display = ('title_preview', 'category', 'content_type', 'table_status', 'views', 'helpful_count', 'is_important', 'is_featured', 'is_published', 'created_at')
    list_filter = ('category', 'content_type', 'is_important', 'is_featured', 'is_published', 'created_at')
    search_fields = ('title', 'short_description', 'content', 'table_title')
    list_editable = ('is_important', 'is_featured', 'is_published')
    prepopulated_fields = {'slug': ('title',)}
    ordering = ('-is_featured', '-is_important', 'display_order', 'title')
    readonly_fields = ('views', 'helpful_count', 'created_at', 'updated_at', 'table_preview')
    inlines = [GuidelineChecklistInline]
    actions = ['reparse_tables']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('category', 'title', 'slug', 'short_description', 'content_type')
        }),
        ('Content', {
            'fields': ('content', 'additional_info'),
            'description': 'Main guideline content (HTML supported)'
        }),
        ('Table Data (Excel/CSV Import)', {
            'fields': ('table_title', 'table_file', 'table_has_header', 'table_preview'),
            'classes': ('collapse',),
            'description': 'Upload Excel (.xlsx, .xls) or CSV file. Table will be automatically parsed and displayed on the public page.'
        }),
        ('Resources', {
            'fields': ('downloadable_file', 'external_link', 'video_url'),
            'classes': ('collapse',),
        }),
        ('Display Settings', {
            'fields': ('is_important', 'is_published', 'is_featured', 'display_order')
        }),
        ('Statistics', {
            'fields': ('views', 'helpful_count'),
            'classes': ('collapse',),
        }),
        ('Metadata', {
            'fields': ('created_by', 'created_at', 'updated_at'),
            'classes': ('collapse',),
        }),
    )
    
    def save_model(self, request, obj, form, change):
        """Auto-set created_by and parse table file"""
        if not change:
            obj.created_by = request.user
        
        # Save first to ensure file is written to disk
        super().save_model(request, obj, form, change)
        
        # Parse table file if uploaded and content type is table
        if obj.table_file and obj.content_type == 'table':
            try:
                from conference.utils.table_parser import parse_table_file
                import os
                
                # Now the file should exist on disk
                file_path = obj.table_file.path
                if os.path.exists(file_path):
                    table_data = parse_table_file(file_path, obj.table_has_header)
                    obj.table_data = table_data
                    # Save again to update table_data
                    obj.save(update_fields=['table_data'])
                    self.message_user(
                        request,
                        f"✅ Table parsed successfully: {table_data['total_rows']} rows × {table_data['total_columns']} columns",
                        messages.SUCCESS
                    )
                else:
                    self.message_user(
                        request,
                        f"⚠️ Table file not found at: {file_path}",
                        messages.WARNING
                    )
            except Exception as e:
                self.message_user(
                    request,
                    f"❌ Error parsing table file: {str(e)}",
                    messages.ERROR
                )
                import traceback
                traceback.print_exc()  # Log full error for debugging
    
    def title_preview(self, obj):
        """Show title with badges"""
        badges = ''
        if obj.is_featured:
            badges += '<span style="background: #ffd700; padding: 2px 8px; border-radius: 10px; font-size: 0.75rem; margin-left: 5px; color: #000;">Featured</span>'
        if obj.is_important:
            badges += '<span style="background: #dc3545; padding: 2px 8px; border-radius: 10px; font-size: 0.75rem; margin-left: 5px; color: white;">Important</span>'
        
        title = obj.title[:60] + '...' if len(obj.title) > 60 else obj.title
        return format_html('<strong>{}</strong>{}', title, badges)
    title_preview.short_description = 'Title'
    
    def table_status(self, obj):
        """Show table data status"""
        if obj.table_data:
            rows = obj.table_data.get('total_rows', 0)
            cols = obj.table_data.get('total_columns', 0)
            return format_html(
                '<span style="background: #28a745; color: white; padding: 3px 10px; border-radius: 12px; font-size: 0.85rem;">'
                '📊 {} rows × {} cols</span>',
                rows, cols
            )
        return format_html('<span style="color: #999;">No table</span>')
    table_status.short_description = 'Table'
    
    def table_preview(self, obj):
        """Show table preview in admin"""
        if not obj.table_data:
            return format_html('<p style="color: #999; font-style: italic;">No table data available. Upload an Excel or CSV file above.</p>')
        
        headers = obj.table_data.get('headers', [])
        rows = obj.table_data.get('rows', [])
        
        # Show first 5 rows only
        preview_rows = rows[:5]
        
        table_html = '<div style="overflow-x: auto; max-width: 100%;">'
        table_html += '<table style="border-collapse: collapse; width: 100%; margin-top: 10px; font-size: 0.9rem;">'
        
        # Headers
        table_html += '<thead><tr style="background: #667eea; color: white;">'
        for header in headers:
            table_html += f'<th style="padding: 10px; border: 1px solid #ddd; text-align: left;">{header}</th>'
        table_html += '</tr></thead>'
        
        # Rows
        table_html += '<tbody>'
        for i, row in enumerate(preview_rows):
            bg_color = '#f8f9fa' if i % 2 == 0 else 'white'
            table_html += f'<tr style="background: {bg_color};">'
            for cell in row:
                table_html += f'<td style="padding: 8px; border: 1px solid #ddd;">{cell}</td>'
            table_html += '</tr>'
        table_html += '</tbody></table>'
        
        if len(rows) > 5:
            table_html += f'<p style="margin-top: 10px; color: #666; font-style: italic;">Showing 5 of {len(rows)} rows</p>'
        
        table_html += '</div>'
        
        return format_html(table_html)
    table_preview.short_description = 'Table Preview'
    
    def reparse_tables(self, request, queryset):
        """Admin action to manually re-parse table files"""
        from conference.utils.table_parser import parse_table_file
        import os
        
        success_count = 0
        error_count = 0
        
        for obj in queryset:
            if obj.table_file:
                try:
                    file_path = obj.table_file.path
                    if os.path.exists(file_path):
                        table_data = parse_table_file(file_path, obj.table_has_header)
                        obj.table_data = table_data
                        obj.save(update_fields=['table_data'])
                        success_count += 1
                    else:
                        error_count += 1
                except Exception as e:
                    error_count += 1
                    self.message_user(
                        request,
                        f"Error parsing {obj.title}: {str(e)}",
                        messages.ERROR
                    )
            else:
                error_count += 1
        
        if success_count > 0:
            self.message_user(
                request,
                f"✅ Successfully re-parsed {success_count} table(s)",
                messages.SUCCESS
            )
        if error_count > 0:
            self.message_user(
                request,
                f"⚠️ {error_count} guideline(s) had no table file or encountered errors",
                messages.WARNING
            )
    reparse_tables.short_description = "Re-parse table files"

# Register with both admin sites
custom_admin_site.register(Guideline, GuidelineAdmin)
admin.site.register(Guideline, GuidelineAdmin)


# =============================================================================
# AWARDS ADMIN
# =============================================================================

@admin.register(AwardCategory, site=custom_admin_site)
class AwardCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'category_type', 'icon_preview', 'awards_count', 'display_order', 'is_active', 'show_on_homepage')
    list_filter = ('category_type', 'is_active', 'show_on_homepage', 'created_at')
    search_fields = ('name', 'description')
    list_editable = ('is_active', 'show_on_homepage')
    prepopulated_fields = {'slug': ('name',)}
    ordering = ('display_order', 'name')
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'slug', 'category_type', 'description')
        }),
        ('Award Details', {
            'fields': ('prize_details', 'eligibility')
        }),
        ('Appearance', {
            'fields': ('icon', 'color')
        }),
        ('Display Settings', {
            'fields': ('display_order', 'is_active', 'show_on_homepage')
        }),
    )
    
    def icon_preview(self, obj):
        """Show icon preview"""
        return format_html('<i class="{}" style="font-size: 1.5rem; color: {};"></i>', obj.icon, obj.color)
    icon_preview.short_description = 'Icon'
    
    def awards_count(self, obj):
        """Count awards in category"""
        count = obj.awards.count()
        return format_html('<span style="font-weight: bold; color: #28a745;">{}</span>', count)
    awards_count.short_description = 'Awards'

# Also register with default admin
admin.site.register(AwardCategory, AwardCategoryAdmin)


class AwardCriteriaInline(admin.TabularInline):
    model = AwardCriteria
    extra = 1
    fields = ('criterion_name', 'description', 'weight_percentage', 'display_order')
    ordering = ('display_order',)


class AwardGalleryInline(admin.TabularInline):
    model = AwardGallery
    extra = 1
    fields = ('image', 'title', 'image_type', 'is_active', 'display_order')
    ordering = ('display_order',)
    readonly_fields = ()


@admin.register(Award, site=custom_admin_site)
class AwardAdmin(admin.ModelAdmin):
    list_display = ('title_preview', 'category', 'year', 'status_badge', 'prize_amount', 'is_featured', 'created_at')
    list_filter = ('category', 'status', 'year', 'is_featured', 'created_at')
    search_fields = ('title', 'description', 'winner_name', 'winning_work_title')
    list_editable = ('is_featured',)
    prepopulated_fields = {'slug': ('title',)}
    ordering = ('-year', '-is_featured', 'display_order')
    readonly_fields = ('created_at', 'updated_at')
    inlines = [AwardCriteriaInline, AwardGalleryInline]
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('category', 'title', 'slug', 'description', 'year')
        }),
        ('Winner Information', {
            'fields': ('winner_name', 'winner_affiliation', 'winner_photo', 'winner_bio'),
            'description': 'Fill this section when winner is announced'
        }),
        ('Winning Work', {
            'fields': ('winning_work_title', 'winning_work_description'),
            'classes': ('collapse',),
        }),
        ('Award Details', {
            'fields': ('prize_amount', 'sponsored_by')
        }),
        ('Timeline', {
            'fields': ('nomination_start', 'nomination_end', 'announcement_date')
        }),
        ('Nomination Settings', {
            'fields': ('nomination_link',),
            'description': 'Add URL for Submit Nomination button (e.g., Google Form, external submission page)'
        }),
        ('Status & Display', {
            'fields': ('status', 'is_featured', 'display_order')
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',),
        }),
    )
    
    def title_preview(self, obj):
        """Show title with badges"""
        badges = ''
        if obj.is_featured:
            badges += '<span style="background: #ffd700; padding: 2px 8px; border-radius: 10px; font-size: 0.75rem; margin-left: 5px; color: #000;">Featured</span>'
        
        title = obj.title[:50] + '...' if len(obj.title) > 50 else obj.title
        return format_html('<strong>{}</strong>{}', title, badges)
    title_preview.short_description = 'Title'
    
    def status_badge(self, obj):
        """Show status with color"""
        colors = {
            'upcoming': '#6c757d',
            'open': '#28a745',
            'closed': '#ffc107',
            'announced': '#007bff',
        }
        color = colors.get(obj.status, '#6c757d')
        return format_html(
            '<span style="background: {}; padding: 4px 12px; border-radius: 15px; color: white; font-size: 0.85rem;">{}</span>',
            color, obj.get_status_display()
        )
    status_badge.short_description = 'Status'

# Also register with default admin
admin.site.register(Award, AwardAdmin)


@admin.register(PastWinner, site=custom_admin_site)
class PastWinnerAdmin(admin.ModelAdmin):
    list_display = ('winner_name', 'award_name', 'year', 'winner_affiliation', 'is_featured', 'display_order')
    list_filter = ('year', 'is_featured')
    search_fields = ('winner_name', 'award_name', 'winner_affiliation', 'work_title')
    list_editable = ('is_featured', 'display_order')
    ordering = ('-year', 'display_order')
    
    fieldsets = (
        ('Award Information', {
            'fields': ('award_name', 'year')
        }),
        ('Winner Information', {
            'fields': ('winner_name', 'winner_affiliation', 'winner_photo')
        }),
        ('Winning Work', {
            'fields': ('work_title', 'work_description')
        }),
        ('Display Settings', {
            'fields': ('is_featured', 'display_order')
        }),
    )

# Also register with default admin
admin.site.register(PastWinner, PastWinnerAdmin)


@admin.register(AwardGallery, site=custom_admin_site)
class AwardGalleryAdmin(admin.ModelAdmin):
    list_display = ('image_preview', 'title', 'image_type', 'year', 'award', 'is_active', 'show_on_hero', 'display_order', 'uploaded_at')
    list_filter = ('image_type', 'year', 'is_active', 'show_on_hero', 'uploaded_at')
    search_fields = ('title', 'description')
    list_editable = ('is_active', 'show_on_hero', 'display_order')
    ordering = ('-year', 'display_order', '-uploaded_at')
    readonly_fields = ('uploaded_at', 'image_preview_large')
    
    fieldsets = (
        ('Image Information', {
            'fields': ('title', 'image', 'image_preview_large', 'image_type', 'description')
        }),
        ('Association', {
            'fields': ('award', 'year'),
            'description': 'Optionally link to a specific award'
        }),
        ('Display Settings', {
            'fields': ('is_active', 'show_on_hero', 'display_order')
        }),
        ('Metadata', {
            'fields': ('uploaded_at',),
            'classes': ('collapse',),
        }),
    )
    
    def image_preview(self, obj):
        """Show small image preview in list"""
        if obj.image:
            return format_html('<img src="{}" style="width: 60px; height: 60px; object-fit: cover; border-radius: 8px; box-shadow: 0 2px 8px rgba(0,0,0,0.1);" />', 
                             obj.image.url)
        return format_html('<span style="color: #999;">No image</span>')
    image_preview.short_description = 'Preview'
    
    def image_preview_large(self, obj):
        """Show larger image preview in detail view"""
        if obj.image:
            return format_html(
                '<div style="margin: 10px 0;">'
                '<img src="{}" style="max-width: 400px; max-height: 300px; border-radius: 10px; box-shadow: 0 4px 12px rgba(0,0,0,0.15);" />'
                '<p style="margin-top: 10px; color: #666; font-size: 0.9rem;"><strong>File:</strong> {}</p>'
                '</div>', 
                obj.image.url,
                obj.image.name
            )
        return format_html('<p style="color: #999;">No image uploaded</p>')
    image_preview_large.short_description = 'Image Preview'

# Also register with default admin
admin.site.register(AwardGallery, AwardGalleryAdmin)


# =============================================================================
# SITE SETTINGS ADMIN
# =============================================================================

@admin.register(SiteSettings, site=custom_admin_site)
class SiteSettingsAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Site Information', {
            'fields': ('site_name', 'site_tagline')
        }),
        ('Logos & Branding', {
            'fields': ('main_logo', 'footer_logo', 'favicon'),
            'description': 'Upload site logos and favicon. Recommended sizes: Logo (200x60px), Favicon (32x32px)'
        }),
        ('Contact Information', {
            'fields': ('contact_email', 'contact_phone', 'contact_address')
        }),
        ('Social Media Links', {
            'fields': ('facebook_url', 'twitter_url', 'linkedin_url', 'instagram_url', 'youtube_url'),
            'classes': ('collapse',)
        }),
        ('Theme Colors', {
            'fields': ('primary_color', 'secondary_color'),
            'description': 'Enter hex color codes (e.g., #a0352f). Changes will affect buttons, headers, and accents.'
        }),
        ('Submit Paper Button', {
            'fields': ('submit_paper_text', 'submit_paper_url'),
            'description': 'Customize the Submit Paper button text and link. Leave URL as #submit-paper for same-page anchor.'
        }),
        ('Become Sponsor Button', {
            'fields': ('sponsor_button_text', 'sponsor_button_url'),
            'description': 'Customize the Become a Sponsor button text and link on the homepage.'
        }),
        ('Contact Page - Venue Details', {
            'fields': ('venue_name', 'venue_address_line1', 'venue_address_line2', 'venue_address_line3'),
            'description': 'Conference venue information displayed on the contact page.'
        }),
        ('Contact Page - Email Addresses', {
            'fields': ('general_email', 'submissions_email', 'registration_email'),
            'description': 'Contact email addresses for different purposes.'
        }),
        ('Contact Page - Phone Numbers', {
            'fields': ('main_phone', 'conference_phone'),
            'description': 'Contact phone numbers displayed on the contact page.'
        }),
        ('Contact Page - Office Hours', {
            'fields': ('office_hours_weekday', 'office_hours_weekend', 'office_hours_timezone'),
            'description': 'Office hours and timezone information.'
        }),
        ('Contact Page - Form Settings', {
            'fields': ('enable_contact_form', 'use_custom_iframe', 'custom_form_url', 'custom_form_height'),
            'description': 'To use Google Form: 1) Open your Google Form, 2) Click Send → Embed HTML → Copy the src URL, 3) Paste it in "Custom form URL", 4) Check "Use custom iframe". The form will replace the default contact form.'
        }),
        ('Contact Page - Map Settings', {
            'fields': ('google_maps_embed_url',),
            'description': 'Google Maps embed URL for venue location. Get it from Google Maps → Share → Embed a map.'
        }),
    )
    
    def has_add_permission(self, request):
        # Only allow one instance
        return not SiteSettings.objects.exists()
    
    def has_delete_permission(self, request, obj=None):
        # Don't allow deletion
        return False
    
    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        # Clear homepage cache when site settings are updated
        cache.delete('homepage_data_v3')

# Register with default admin too
admin.site.register(SiteSettings, SiteSettingsAdmin)


@admin.register(HeroSlide, site=custom_admin_site)
class HeroSlideAdmin(admin.ModelAdmin):
    list_display = ('slide_preview', 'title', 'slide_type', 'is_active', 'display_order', 'created_at')
    list_filter = ('slide_type', 'is_active', 'text_position')
    search_fields = ('title', 'subtitle')
    list_editable = ('is_active', 'display_order')
    ordering = ('display_order', '-created_at')
    
    # Important: Enable file upload handling
    save_as = True
    save_on_top = True
    
    fieldsets = (
        ('Slide Information', {
            'fields': ('title', 'subtitle', 'slide_type')
        }),
        ('Image Slide', {
            'fields': ('image',),
            'description': 'Upload background image for image-type slides. Recommended size: 1920x1080px'
        }),
        ('Video Slide', {
            'fields': ('video_file', 'video_url', 'video_thumbnail'),
            'description': 'Either upload a video file (MP4/WebM) OR provide a YouTube/Vimeo URL. Add thumbnail for better loading.'
        }),
        ('Call to Action Button', {
            'fields': ('cta_text', 'cta_url', 'cta_style'),
            'classes': ('collapse',)
        }),
        ('Text Overlay Settings', {
            'fields': ('text_position', 'text_color', 'show_overlay'),
            'classes': ('collapse',)
        }),
        ('Display Settings', {
            'fields': ('display_order', 'is_active')
        }),
    )
    
    def save_model(self, request, obj, form, change):
        """Override save to ensure image is saved properly"""
        super().save_model(request, obj, form, change)
        # Clear homepage cache when slides are updated
        from django.core.cache import cache
        cache.delete('homepage_data_v3')
    
    def slide_preview(self, obj):
        """Show slide thumbnail"""
        if obj.slide_type == 'image' and obj.image:
            return format_html(
                '<img src="{}" style="width: 100px; height: 60px; object-fit: cover; border-radius: 5px;"/>',
                obj.image.url
            )
        elif obj.slide_type == 'video' and obj.video_thumbnail:
            return format_html(
                '<div style="position: relative;"><img src="{}" style="width: 100px; height: 60px; object-fit: cover; border-radius: 5px;"/>'
                '<i class="fas fa-play-circle" style="position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%); color: white; font-size: 24px;"></i></div>',
                obj.video_thumbnail.url
            )
        elif obj.slide_type == 'video':
            return format_html('<i class="fas fa-video" style="font-size: 40px; color: #a0352f;"></i>')
        return format_html('<i class="fas fa-image" style="font-size: 40px; color: #ccc;"></i>')
    slide_preview.short_description = 'Preview'

# Register with default admin
admin.site.register(HeroSlide, HeroSlideAdmin)


@admin.register(SliderSettings, site=custom_admin_site)
class SliderSettingsAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Autoplay Settings', {
            'fields': ('autoplay', 'autoplay_speed', 'transition_speed', 'transition_effect')
        }),
        ('Navigation Controls', {
            'fields': ('show_arrows', 'show_dots', 'pause_on_hover')
        }),
        ('Mobile Settings', {
            'fields': ('autoplay_mobile', 'show_arrows_mobile'),
            'classes': ('collapse',)
        }),
        ('Slider Dimensions', {
            'fields': ('slider_height_desktop', 'slider_height_mobile'),
            'description': 'Height in pixels'
        }),
        ('Performance', {
            'fields': ('lazy_load', 'preload_slides'),
            'classes': ('collapse',)
        }),
    )
    
    def has_add_permission(self, request):
        # Only allow one instance
        return not SliderSettings.objects.exists()
    
    def has_delete_permission(self, request, obj=None):
        # Don't allow deletion
        return False
    
    class Media:
        css = {
            'all': ('admin/css/slider-settings.css',)
        }

# Register with default admin
admin.site.register(SliderSettings, SliderSettingsAdmin)

@admin.register(MarqueeText)
class MarqueeTextAdmin(admin.ModelAdmin):
    list_display = ['text_preview', 'is_enabled', 'background_color', 'text_color', 'animation_speed', 'updated_at']
    list_editable = ['is_enabled']
    fieldsets = (
        ('Marquee Content', {
            'fields': ('text', 'is_enabled')
        }),
        ('Styling', {
            'fields': ('background_color', 'text_color', 'animation_speed'),
            'description': 'Customize the appearance and animation speed of the marquee'
        }),
    )
    
    def text_preview(self, obj):
        return obj.text[:50] + "..." if len(obj.text) > 50 else obj.text
    text_preview.short_description = 'Marquee Text'
    
    def has_add_permission(self, request):
        # Only allow one marquee text instance
        if MarqueeText.objects.exists():
            return False
        return super().has_add_permission(request)
    
    def has_delete_permission(self, request, obj=None):
        # Prevent deletion - only allow disabling
        return False

@admin.register(ConferenceTopic)
class ConferenceTopicAdmin(admin.ModelAdmin):
    list_display = ['title', 'icon_preview', 'display_order', 'is_active', 'updated_at']
    list_editable = ['display_order', 'is_active']
    list_filter = ['is_active']
    search_fields = ['title', 'description']
    ordering = ['display_order', 'title']
    
    fieldsets = (
        ('Topic Information', {
            'fields': ('title', 'description', 'icon_class')
        }),
        ('Display Settings', {
            'fields': ('display_order', 'is_active')
        }),
    )
    
    def icon_preview(self, obj):
        return format_html('<i class="{}"></i> {}', obj.icon_class, obj.icon_class)
    icon_preview.short_description = 'Icon'


@admin.register(VisitorCounter)
class VisitorCounterAdmin(admin.ModelAdmin):
    list_display = ['ip_address', 'visit_count', 'first_visit', 'last_visit', 'user_agent_preview']
    list_filter = ['first_visit', 'last_visit']
    search_fields = ['ip_address', 'session_key']
    ordering = ['-last_visit']
    readonly_fields = ['ip_address', 'user_agent', 'session_key', 'first_visit', 'last_visit', 'visit_count']
    
    fieldsets = (
        ('Visitor Information', {
            'fields': ('ip_address', 'session_key', 'visit_count')
        }),
        ('Visit Details', {
            'fields': ('first_visit', 'last_visit', 'user_agent')
        }),
    )
    
    def user_agent_preview(self, obj):
        """Show truncated user agent"""
        ua = obj.user_agent[:50] + '...' if len(obj.user_agent) > 50 else obj.user_agent
        return ua
    user_agent_preview.short_description = 'Browser'
    
    def has_add_permission(self, request):
        """Prevent manual adding of visitors"""
        return False
    
    def has_delete_permission(self, request, obj=None):
        """Allow deletion to clean up old records"""
        return request.user.is_superuser
    
    def changelist_view(self, request, extra_context=None):
        """Add total visitor count to admin page"""
        extra_context = extra_context or {}
        extra_context['total_visitors'] = VisitorCounter.get_total_visitors()
        extra_context['today_visitors'] = VisitorCounter.get_today_visitors()
        return super().changelist_view(request, extra_context)


# =============================================================================
# REGISTRATION ADMIN
# =============================================================================

@admin.register(RegistrationCategory)
class RegistrationCategoryAdmin(admin.ModelAdmin):
    """Admin for registration categories"""
    list_display = [
        'display_name', 'category_type', 'currency', 
        'early_bird_rates', 'standard_rates', 'early_bird_deadline',
        'is_active', 'display_order'
    ]
    list_filter = ['is_active', 'currency', 'requires_paper', 'requires_student_id']
    search_fields = ['display_name', 'category_type', 'description']
    list_editable = ['is_active', 'display_order']
    ordering = ['display_order', 'category_type']
    
    fieldsets = (
        ('Category Information', {
            'fields': ('category_type', 'display_name', 'description', 'currency')
        }),
        ('Early Bird Pricing', {
            'fields': ('early_bird_ieee_member', 'early_bird_non_ieee', 'early_bird_deadline'),
            'description': 'Rates applicable until early bird deadline'
        }),
        ('Standard Pricing', {
            'fields': ('standard_ieee_member', 'standard_non_ieee'),
            'description': 'Rates applicable after early bird deadline'
        }),
        ('Settings', {
            'fields': ('is_active', 'display_order', 'requires_paper', 'requires_student_id')
        }),
    )
    
    def early_bird_rates(self, obj):
        """Display early bird rates"""
        symbol = '₹' if obj.currency == 'INR' else '$'
        return format_html(
            '<strong>IEEE:</strong> {}{} | <strong>Non-IEEE:</strong> {}{}',
            symbol, obj.early_bird_ieee_member, symbol, obj.early_bird_non_ieee
        )
    early_bird_rates.short_description = 'Early Bird Rates'
    
    def standard_rates(self, obj):
        """Display standard rates"""
        symbol = '₹' if obj.currency == 'INR' else '$'
        return format_html(
            '<strong>IEEE:</strong> {}{} | <strong>Non-IEEE:</strong> {}{}',
            symbol, obj.standard_ieee_member, symbol, obj.standard_non_ieee
        )
    standard_rates.short_description = 'Standard Rates'
    
    actions = ['activate_categories', 'deactivate_categories', clear_site_cache]
    
    def activate_categories(self, request, queryset):
        """Activate selected categories"""
        count = queryset.update(is_active=True)
        self.message_user(request, f'{count} category/categories activated.', messages.SUCCESS)
    activate_categories.short_description = 'Activate selected categories'
    
    def deactivate_categories(self, request, queryset):
        """Deactivate selected categories"""
        count = queryset.update(is_active=False)
        self.message_user(request, f'{count} category/categories deactivated.', messages.SUCCESS)
    deactivate_categories.short_description = 'Deactivate selected categories'


@admin.register(ConferenceRegistration)
class ConferenceRegistrationAdmin(admin.ModelAdmin):
    """Admin for conference registrations"""
    list_display = [
        'registration_id', 'get_full_name', 'email', 'category',
        'status_badge', 'payment_amount', 'currency',
        'is_ieee_member', 'has_paper', 'created_at'
    ]
    list_filter = [
        'status', 'category', 'is_ieee_member', 'is_student',
        'has_paper', 'payment_method', 'created_at'
    ]
    search_fields = [
        'registration_id', 'first_name', 'last_name', 'email',
        'organization', 'paper_id', 'transaction_id'
    ]
    readonly_fields = [
        'registration_id', 'created_at', 'updated_at', 'confirmed_by', 'confirmed_at'
    ]
    date_hierarchy = 'created_at'
    
    fieldsets = (
        ('Registration Information', {
            'fields': ('registration_id', 'category', 'status', 'created_at', 'updated_at')
        }),
        ('Personal Information', {
            'fields': (
                'title', 'first_name', 'last_name', 'email',
                'phone', 'alternate_phone'
            )
        }),
        ('Professional Information', {
            'fields': (
                'organization', 'designation', 'department',
                'country', 'state', 'city', 'address', 'postal_code'
            )
        }),
        ('IEEE Membership', {
            'fields': ('is_ieee_member', 'ieee_membership_id'),
            'classes': ['collapse']
        }),
        ('Student Information', {
            'fields': ('is_student', 'student_id', 'student_id_document'),
            'classes': ['collapse']
        }),
        ('Paper Information', {
            'fields': ('has_paper', 'paper_id', 'paper_title', 'additional_pages'),
            'classes': ['collapse']
        }),
        ('Payment Information', {
            'fields': (
                'payment_method', 'payment_amount', 'currency',
                'payment_date', 'transaction_id', 'payment_receipt', 'payment_notes'
            )
        }),
        ('Additional Information', {
            'fields': ('special_requirements', 'accommodation_required'),
            'classes': ['collapse']
        }),
        ('Admin Section', {
            'fields': ('admin_notes', 'confirmed_by', 'confirmed_at'),
            'classes': ['collapse']
        }),
    )
    
    actions = [
        'mark_as_confirmed', 'mark_as_pending', 'mark_as_cancelled',
        'export_registrations_csv', 'send_confirmation_email',
        clear_site_cache
    ]
    
    def status_badge(self, obj):
        """Display status as colored badge"""
        badge_class = obj.get_status_badge_class()
        return format_html(
            '<span class="badge bg-{}">{}</span>',
            badge_class, obj.get_status_display()
        )
    status_badge.short_description = 'Status'
    
    def mark_as_confirmed(self, request, queryset):
        """Mark registrations as confirmed"""
        from django.utils import timezone
        count = queryset.update(
            status='confirmed',
            confirmed_by=request.user,
            confirmed_at=timezone.now()
        )
        self.message_user(request, f'{count} registration(s) confirmed.', messages.SUCCESS)
    mark_as_confirmed.short_description = 'Mark as Confirmed'
    
    def mark_as_pending(self, request, queryset):
        """Mark registrations as pending"""
        count = queryset.update(status='pending')
        self.message_user(request, f'{count} registration(s) marked as pending.', messages.INFO)
    mark_as_pending.short_description = 'Mark as Pending'
    
    def mark_as_cancelled(self, request, queryset):
        """Mark registrations as cancelled"""
        count = queryset.update(status='cancelled')
        self.message_user(request, f'{count} registration(s) cancelled.', messages.WARNING)
    mark_as_cancelled.short_description = 'Mark as Cancelled'
    
    def export_registrations_csv(self, request, queryset):
        """Export registrations to CSV"""
        import csv
        from django.http import HttpResponse
        
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="registrations.csv"'
        
        writer = csv.writer(response)
        writer.writerow([
            'Registration ID', 'Name', 'Email', 'Phone', 'Organization',
            'Category', 'Status', 'IEEE Member', 'Paper ID', 'Amount',
            'Payment Method', 'Transaction ID', 'Created At'
        ])
        
        for reg in queryset:
            writer.writerow([
                reg.registration_id, reg.get_full_name(), reg.email, reg.phone,
                reg.organization, reg.category.display_name, reg.get_status_display(),
                'Yes' if reg.is_ieee_member else 'No', reg.paper_id or '-',
                f"{reg.payment_amount} {reg.currency}", reg.payment_method or '-',
                reg.transaction_id or '-', reg.created_at.strftime('%Y-%m-%d %H:%M')
            ])
        
        return response
    export_registrations_csv.short_description = 'Export to CSV'
    
    def send_confirmation_email(self, request, queryset):
        """Send confirmation email to registrants"""
        # This would integrate with your email system
        count = queryset.filter(status='confirmed').count()
        self.message_user(
            request,
            f'Confirmation emails will be sent to {count} registrant(s).',
            messages.INFO
        )
    send_confirmation_email.short_description = 'Send Confirmation Email'
    
    def changelist_view(self, request, extra_context=None):
        """Add statistics to changelist"""
        extra_context = extra_context or {}
        extra_context['total_registrations'] = ConferenceRegistration.objects.count()
        extra_context['confirmed_registrations'] = ConferenceRegistration.objects.filter(status='confirmed').count()
        extra_context['pending_registrations'] = ConferenceRegistration.objects.filter(status='pending').count()
        return super().changelist_view(request, extra_context)


@admin.register(RegistrationSettings)
class RegistrationSettingsAdmin(admin.ModelAdmin):
    """Admin for registration settings"""
    
    fieldsets = (
        ('Registration Status', {
            'fields': ('registration_open', 'registration_message'),
            'description': 'Control whether registration is open and display a message to users'
        }),
        ('Payment Links', {
            'fields': ('pay_now_indian_link', 'pay_now_international_link', 'show_payment_buttons'),
            'description': 'Payment gateway links for Indian and International authors'
        }),
        ('Bank Account Details', {
            'fields': (
                'bank_name', 'account_name', 'account_number',
                'ifsc_code', 'swift_code', 'bank_address', 'show_account_details'
            ),
            'description': 'Bank account information for manual transfers'
        }),
        ('Important Information Section', {
            'fields': ('important_info_title', 'important_info_content', 'show_important_info'),
            'description': 'Important registration information displayed on the page (HTML allowed)',
            'classes': ['collapse']
        }),
        ('Contact Information', {
            'fields': ('registration_email', 'registration_phone')
        }),
        ('Limits & Settings', {
            'fields': (
                'max_papers_per_author', 'max_additional_pages',
                'early_bird_deadline', 'show_early_bird_countdown'
            )
        }),
        ('Display Settings', {
            'fields': ('show_registration_process',),
            'description': 'Control visibility of various sections'
        }),
        ('Form Mode Settings', {
            'fields': (
                'use_google_form', 'show_default_form', 'google_form_url',
                'google_form_height', 'form_mode_message'
            ),
            'description': 'Choose between default form and Google Form. You can show both, only one, or switch between them.',
            'classes': ['collapse']
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ['collapse']
        }),
    )
    
    readonly_fields = ['created_at', 'updated_at']
    
    def has_add_permission(self, request):
        """Only allow one settings instance"""
        return not RegistrationSettings.objects.exists()
    
    def has_delete_permission(self, request, obj=None):
        """Prevent deletion of settings"""
        return False


@admin.register(RegistrationFeesTable)
class RegistrationFeesTableAdmin(admin.ModelAdmin):
    """Admin for registration fees table"""
    list_display = ['display_name', 'participant_type', 'early_bird_ieee', 'early_bird_non_ieee', 
                    'regular_ieee', 'regular_non_ieee', 'is_active', 'is_highlighted', 'display_order']
    list_filter = ['is_active', 'is_highlighted', 'participant_type']
    search_fields = ['display_name', 'participant_type', 'notes']
    list_editable = ['is_active', 'is_highlighted', 'display_order']
    ordering = ['display_order', 'participant_type']
    
    fieldsets = (
        ('Participant Information', {
            'fields': ('participant_type', 'display_name', 'notes'),
            'description': 'Define the participant type and display name for the fees table'
        }),
        ('Early Bird Fees', {
            'fields': ('early_bird_ieee', 'early_bird_non_ieee'),
            'description': 'Early bird registration fees (e.g., ₹6000 or $200)'
        }),
        ('Regular Fees', {
            'fields': ('regular_ieee', 'regular_non_ieee'),
            'description': 'Regular registration fees after early bird deadline'
        }),
        ('Display Settings', {
            'fields': ('is_active', 'is_highlighted', 'display_order'),
            'description': 'Control visibility and appearance in the fees table'
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ['collapse']
        }),
    )
    
    readonly_fields = ['created_at', 'updated_at']
    
    actions = ['activate_rows', 'deactivate_rows', 'highlight_rows', 'unhighlight_rows']
    
    @admin.action(description='Activate selected rows')
    def activate_rows(self, request, queryset):
        updated = queryset.update(is_active=True)
        self.message_user(request, f'{updated} row(s) activated successfully.')
    
    @admin.action(description='Deactivate selected rows')
    def deactivate_rows(self, request, queryset):
        updated = queryset.update(is_active=False)
        self.message_user(request, f'{updated} row(s) deactivated successfully.')
    
    @admin.action(description='Highlight selected rows')
    def highlight_rows(self, request, queryset):
        updated = queryset.update(is_highlighted=True)
        self.message_user(request, f'{updated} row(s) highlighted successfully.')
    
    @admin.action(description='Remove highlight from selected rows')
    def unhighlight_rows(self, request, queryset):
        updated = queryset.update(is_highlighted=False)
        self.message_user(request, f'{updated} row(s) unhighlighted successfully.')


@admin.register(DownloadResource)
class DownloadResourceAdmin(admin.ModelAdmin):
    """Admin for download resources"""
    list_display = ['title', 'category', 'file_type', 'file_size', 'author', 'downloads', 'is_featured', 'is_active', 'created_at']
    list_filter = ['category', 'is_active', 'is_featured', 'created_at']
    search_fields = ['title', 'description', 'author', 'category']
    list_editable = ['is_featured', 'is_active']
    readonly_fields = ['downloads', 'created_at', 'updated_at']
    
    fieldsets = (
        ('Resource Information', {
            'fields': ('title', 'description', 'category', 'version', 'author')
        }),
        ('File', {
            'fields': ('file', 'file_type', 'file_size', 'thumbnail')
        }),
        ('Additional Details', {
            'fields': ('related_url',),
            'classes': ['collapse']
        }),
        ('Status & Stats', {
            'fields': ('is_active', 'is_featured', 'downloads')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ['collapse']
        })
    )
    
    actions = ['activate_resources', 'deactivate_resources', 'feature_resources', 'unfeature_resources']
    
    def activate_resources(self, request, queryset):
        updated = queryset.update(is_active=True)
        self.message_user(request, f'{updated} resource(s) activated successfully.')
    activate_resources.short_description = 'Activate selected resources'
    
    def deactivate_resources(self, request, queryset):
        updated = queryset.update(is_active=False)
        self.message_user(request, f'{updated} resource(s) deactivated successfully.')
    deactivate_resources.short_description = 'Deactivate selected resources'
    
    def feature_resources(self, request, queryset):
        updated = queryset.update(is_featured=True)
        self.message_user(request, f'{updated} resource(s) marked as featured.')
    feature_resources.short_description = 'Mark as featured'
    
    def unfeature_resources(self, request, queryset):
        updated = queryset.update(is_featured=False)
        self.message_user(request, f'{updated} resource(s) unmarked as featured.')
    unfeature_resources.short_description = 'Remove featured status'


@admin.register(Speaker)
class SpeakerAdmin(admin.ModelAdmin):
    """Admin for conference speakers"""
    list_display = ['name', 'title', 'organization', 'speaker_type', 'enable_bio_page', 'page_views', 'is_featured', 'is_published', 'display_order']
    list_editable = ['display_order', 'enable_bio_page', 'is_featured', 'is_published']
    list_filter = ['speaker_type', 'is_featured', 'is_published', 'enable_bio_page', 'country', 'created_at']
    search_fields = ['name', 'title', 'organization', 'bio', 'detailed_bio', 'expertise']
    ordering = ['display_order', 'name']
    readonly_fields = ['slug', 'page_views', 'last_viewed', 'view_bio_page_link', 'created_at', 'updated_at']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'slug', 'title', 'organization', 'country', 'photo')
        }),
        ('Biography', {
            'fields': ('bio', 'detailed_bio', 'expertise', 'research_interests'),
            'description': 'Bio shows on speakers page. Detailed bio shows on dedicated bio page.'
        }),
        ('Talk Details', {
            'fields': ('speaker_type', 'talk_title', 'talk_abstract', 'session_time'),
            'classes': ('collapse',)
        }),
        ('Extended Information', {
            'fields': ('education', 'publications', 'awards'),
            'classes': ('collapse',)
        }),
        ('Contact & Social Media', {
            'fields': ('email', 'website', 'linkedin', 'twitter', 'google_scholar', 'orcid', 'researchgate'),
            'classes': ('collapse',)
        }),
        ('Display Settings', {
            'fields': ('enable_bio_page', 'view_bio_page_link', 'is_featured', 'is_published', 'display_order'),
        }),
        ('Analytics', {
            'fields': ('page_views', 'last_viewed'),
            'classes': ('collapse',)
        }),
        ('Administrative', {
            'fields': ('created_by', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    actions = ['publish_speakers', 'unpublish_speakers', 'feature_speakers', 'unfeature_speakers', 'enable_bio_pages', 'disable_bio_pages']
    
    def view_bio_page_link(self, obj):
        """Link to view the bio page"""
        if obj.pk and obj.enable_bio_page:
            from django.urls import reverse
            url = reverse('conference:speaker_bio', kwargs={'slug': obj.slug})
            return format_html('<a href="{}" target="_blank" class="button">View Bio Page</a>', url)
        return "Save to generate bio page"
    view_bio_page_link.short_description = 'Bio Page'
    
    def save_model(self, request, obj, form, change):
        """Auto-assign created_by on creation"""
        if not change:  # Only on creation
            obj.created_by = request.user
        super().save_model(request, obj, form, change)
    
    def publish_speakers(self, request, queryset):
        updated = queryset.update(is_published=True)
        self.message_user(request, f'{updated} speaker(s) published successfully.')
    publish_speakers.short_description = 'Publish selected speakers'
    
    def unpublish_speakers(self, request, queryset):
        updated = queryset.update(is_published=False)
        self.message_user(request, f'{updated} speaker(s) unpublished successfully.')
    unpublish_speakers.short_description = 'Unpublish selected speakers'
    
    def feature_speakers(self, request, queryset):
        updated = queryset.update(is_featured=True)
        self.message_user(request, f'{updated} speaker(s) marked as featured.')
    feature_speakers.short_description = 'Mark as featured'
    
    def unfeature_speakers(self, request, queryset):
        updated = queryset.update(is_featured=False)
        self.message_user(request, f'{updated} speaker(s) unmarked as featured.')
    unfeature_speakers.short_description = 'Remove featured status'
    
    def enable_bio_pages(self, request, queryset):
        updated = queryset.update(enable_bio_page=True)
        self.message_user(request, f'{updated} speaker(s) bio pages enabled.')
    enable_bio_pages.short_description = 'Enable bio pages'
    
    def disable_bio_pages(self, request, queryset):
        updated = queryset.update(enable_bio_page=False)
        self.message_user(request, f'{updated} speaker(s) bio pages disabled.')
    disable_bio_pages.short_description = 'Disable bio pages'


@admin.register(LoadingPageSettings)
class LoadingPageSettingsAdmin(admin.ModelAdmin):
    """Admin for loading page customization"""
    
    fieldsets = (
        ('Loading Text Content', {
            'fields': ('loading_title', 'loading_subtitle', 'loading_message'),
            'description': 'Customize the text displayed on the loading page'
        }),
        ('Tagline & Dates', {
            'fields': ('show_tagline', 'tagline_text'),
        }),
        ('Logo Settings', {
            'fields': ('show_logo', 'logo'),
            'description': 'Upload a custom logo or use default conference logo'
        }),
        ('Animation Settings', {
            'fields': ('animation_type', 'show_progress_text'),
            'description': 'Choose the loading animation style'
        }),
        ('Color Scheme', {
            'fields': ('background_color', 'text_color', 'spinner_color'),
            'description': 'Customize colors (use hex codes like #a0352f)'
        }),
        ('Timing Settings', {
            'fields': ('minimum_duration', 'fade_out_duration'),
            'description': 'Control loading page timing (in milliseconds)'
        }),
        ('Advanced Styling', {
            'fields': ('custom_css',),
            'classes': ('collapse',),
            'description': 'Add custom CSS for advanced styling (optional)'
        }),
        ('Footer Settings', {
            'fields': ('show_footer', 'footer_text', 'footer_link'),
            'description': 'Customize the footer text and link on loading page'
        }),
        ('Status', {
            'fields': ('is_active',),
            'description': 'Enable or disable the loading page globally'
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    readonly_fields = ('created_at', 'updated_at')
    
    def has_add_permission(self, request):
        # Only allow one instance
        return not LoadingPageSettings.objects.exists()
    
    def has_delete_permission(self, request, obj=None):
        # Don't allow deletion of settings
        return False


@admin.register(AboutPage)
class AboutPageAdmin(admin.ModelAdmin):
    list_display = ['hero_title', 'is_active', 'updated_at']
    
    fieldsets = (
        ('Hero Section', {
            'fields': ('hero_title', 'hero_subtitle', 'hero_description', 'hero_image'),
            'description': 'Customize the hero section at the top of the about page'
        }),
        ('Conference Overview', {
            'fields': ('overview_title', 'overview_lead', 'overview_content'),
            'description': 'Main overview content about the conference'
        }),
        ('Vision', {
            'fields': ('vision_title', 'vision_content', 'vision_icon'),
        }),
        ('Mission', {
            'fields': ('mission_title', 'mission_content', 'mission_icon'),
        }),
        ('Statistics Section', {
            'fields': (
                'show_statistics',
                ('stat_1_number', 'stat_1_label', 'stat_1_icon'),
                ('stat_2_number', 'stat_2_label', 'stat_2_icon'),
                ('stat_3_number', 'stat_3_label', 'stat_3_icon'),
                ('stat_4_number', 'stat_4_label', 'stat_4_icon'),
            ),
            'description': 'Conference statistics displayed prominently'
        }),
        ('Section Visibility', {
            'fields': ('show_objectives', 'show_university_info'),
            'description': 'Control which sections are displayed'
        }),
        ('SEO Settings', {
            'fields': ('meta_description', 'meta_keywords'),
            'classes': ('collapse',),
            'description': 'Search engine optimization'
        }),
        ('Status', {
            'fields': ('is_active',),
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    readonly_fields = ('created_at', 'updated_at')
    actions = [clear_site_cache]
    
    def has_add_permission(self, request):
        return not AboutPage.objects.exists()
    
    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(AboutObjective)
class AboutObjectiveAdmin(admin.ModelAdmin):
    list_display = ['title', 'order', 'color', 'is_active']
    list_editable = ['order', 'is_active']
    list_filter = ['is_active', 'color']
    search_fields = ['title', 'description']
    ordering = ['order', 'id']
    actions = [clear_site_cache]
    
    fieldsets = (
        ('Objective Details', {
            'fields': ('title', 'description', 'order')
        }),
        ('Styling', {
            'fields': ('icon', 'color'),
            'description': 'Icon: FontAwesome class (e.g., fas fa-lightbulb). Color: Bootstrap class (primary, success, warning, info, danger)'
        }),
        ('Status', {
            'fields': ('is_active',),
        }),
    )


@admin.register(SponsorsPageSettings)
class SponsorsPageSettingsAdmin(admin.ModelAdmin):
    list_display = ['hero_title', 'is_active', 'updated_at']
    
    fieldsets = (
        ('Hero Section', {
            'fields': ('hero_title', 'hero_subtitle'),
            'description': 'Customize the hero section of the sponsors page'
        }),
        ('Sponsorship Contact Information', {
            'fields': (
                'sponsorship_manager_name',
                'sponsorship_manager_email',
                'sponsorship_manager_phone',
            ),
            'description': 'Contact details for sponsorship manager'
        }),
        ('General Inquiry Contact', {
            'fields': (
                'general_inquiry_email',
                'general_inquiry_response_time',
            ),
        }),
        ('Call-to-Action Buttons', {
            'fields': (
                ('contact_button_text', 'contact_button_url'),
                ('prospectus_button_text', 'prospectus_file'),
            ),
            'description': 'Customize CTA buttons and links'
        }),
        ('Section Visibility', {
            'fields': (
                'show_partnership_opportunities',
                'show_why_sponsor',
                'show_contact_section',
            ),
            'description': 'Control which sections are displayed'
        }),
        ('SEO', {
            'fields': ('meta_description',),
            'classes': ('collapse',),
        }),
        ('Status', {
            'fields': ('is_active',),
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    readonly_fields = ('created_at', 'updated_at')
    actions = [clear_site_cache]
    
    def has_add_permission(self, request):
        return not SponsorsPageSettings.objects.exists()
    
    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(PageVisitLog)
class PageVisitLogAdmin(admin.ModelAdmin):
    list_display = ['timestamp', 'ip_address', 'url_path_display', 'browser_info_display', 
                    'device_type', 'location_display', 'is_authenticated', 'username']
    list_filter = ['timestamp', 'device_type', 'browser', 'os', 'is_authenticated']
    search_fields = ['ip_address', 'url_path', 'username', 'city', 'country']
    date_hierarchy = 'timestamp'
    ordering = ['-timestamp']
    readonly_fields = ['ip_address', 'user_agent', 'url_path', 'full_url', 'http_method', 
                       'referrer', 'country', 'city', 'device_type', 'browser', 'os', 
                       'timestamp', 'response_time', 'session_key', 'is_authenticated', 'username']
    
    fieldsets = (
        ('Visit Information', {
            'fields': ('timestamp', 'ip_address', 'session_key', 'is_authenticated', 'username')
        }),
        ('Request Details', {
            'fields': ('url_path', 'full_url', 'http_method', 'referrer', 'response_time')
        }),
        ('Browser & Device', {
            'fields': ('user_agent', 'browser', 'os', 'device_type')
        }),
        ('Location', {
            'fields': ('country', 'city'),
            'classes': ('collapse',)
        }),
    )
    
    def url_path_display(self, obj):
        """Truncate long URLs for display"""
        path = obj.url_path
        return path[:50] + '...' if len(path) > 50 else path
    url_path_display.short_description = 'Page URL'
    
    def browser_info_display(self, obj):
        """Display browser information"""
        return obj.browser_info
    browser_info_display.short_description = 'Browser/OS'
    
    def location_display(self, obj):
        """Display location information"""
        return obj.location_info
    location_display.short_description = 'Location'
    
    def has_add_permission(self, request):
        """Prevent manual adding of page visit logs"""
        return False
    
    def has_delete_permission(self, request, obj=None):
        """Allow deletion to clean up old logs"""
        return request.user.is_superuser
    
    def changelist_view(self, request, extra_context=None):
        """Add statistics to admin page"""
        extra_context = extra_context or {}
        extra_context['total_page_visits'] = PageVisitLog.get_total_visits()
        extra_context['today_page_visits'] = PageVisitLog.get_today_visits()
        extra_context['unique_visitors_today'] = PageVisitLog.get_unique_visitors_today()
        extra_context['popular_pages'] = PageVisitLog.get_popular_pages(limit=5)
        return super().changelist_view(request, extra_context)




@admin.register(SitemapLink)
class SitemapLinkAdmin(admin.ModelAdmin):
    list_display = ['name', 'url', 'icon_preview', 'display_order', 'is_active', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['name', 'url', 'description']
    list_editable = ['display_order', 'is_active']
    ordering = ['display_order', 'name']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'url', 'description')
        }),
        ('Visual Settings', {
            'fields': ('icon',)
        }),
        ('Display Settings', {
            'fields': ('display_order', 'is_active')
        }),
    )
    
    def icon_preview(self, obj):
        return format_html('<i class=\"fas {}\"></i> {}', obj.icon, obj.icon)
    icon_preview.short_description = 'Icon'
