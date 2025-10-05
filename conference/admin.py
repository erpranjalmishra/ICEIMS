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
    AwardCategory, Award, AwardCriteria, PastWinner,
    SiteSettings, HeroSlide, SliderSettings
)

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
    list_display = ['name', 'title', 'organization', 'get_level_name_display', 'hierarchy_level', 'order', 'is_active']
    list_editable = ['order', 'is_active']
    list_filter = ['organization', 'hierarchy_level', 'role', 'is_active']
    search_fields = ['name', 'title', 'organization']
    ordering = ['hierarchy_level', 'order']
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'title', 'organization', 'image')
        }),
        ('Hierarchy & Role', {
            'fields': ('hierarchy_level', 'role', 'order'),
            'description': 'Assign a hierarchy level. You can add more levels in the "Hierarchy Levels" section.'
        }),
        ('Contact Information', {
            'fields': ('email', 'phone'),
            'classes': ('collapse',)
        }),
        ('Additional Details', {
            'fields': ('bio', 'is_active'),
            'classes': ('collapse',)
        }),
    )
    
    def get_level_name_display(self, obj):
        """Show the hierarchy level name instead of just the number"""
        return obj.get_hierarchy_level_name()
    get_level_name_display.short_description = 'Level Name'
    get_level_name_display.admin_order_field = 'hierarchy_level'

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


@admin.register(Award, site=custom_admin_site)
class AwardAdmin(admin.ModelAdmin):
    list_display = ('title_preview', 'category', 'year', 'status_badge', 'prize_amount', 'is_featured', 'created_at')
    list_filter = ('category', 'status', 'year', 'is_featured', 'created_at')
    search_fields = ('title', 'description', 'winner_name', 'winning_work_title')
    list_editable = ('is_featured',)
    prepopulated_fields = {'slug': ('title',)}
    ordering = ('-year', '-is_featured', 'display_order')
    readonly_fields = ('created_at', 'updated_at')
    inlines = [AwardCriteriaInline]
    
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
