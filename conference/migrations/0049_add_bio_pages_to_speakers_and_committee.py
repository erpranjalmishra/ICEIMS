# Generated migration for bio pages functionality

from django.db import migrations, models
import django.db.models.deletion
from django.utils.text import slugify


def generate_slugs_committee(apps, schema_editor):
    """Generate slugs for existing committee members"""
    CommitteeMember = apps.get_model('conference', 'CommitteeMember')
    for member in CommitteeMember.objects.all():
        if not member.slug:
            base_slug = slugify(member.name)
            slug = base_slug
            counter = 1
            while CommitteeMember.objects.filter(slug=slug).exclude(pk=member.pk).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            member.slug = slug
            member.save(update_fields=['slug'])


def generate_slugs_speaker(apps, schema_editor):
    """Generate slugs for existing speakers"""
    Speaker = apps.get_model('conference', 'Speaker')
    for speaker in Speaker.objects.all():
        if not speaker.slug:
            base_slug = slugify(speaker.name)
            slug = base_slug
            counter = 1
            while Speaker.objects.filter(slug=slug).exclude(pk=speaker.pk).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            speaker.slug = slug
            speaker.save(update_fields=['slug'])


class Migration(migrations.Migration):

    dependencies = [
        ('conference', '0048_registrationfeestable'),
    ]

    operations = [
        # CommitteeMember fields
        migrations.AddField(
            model_name='committeemember',
            name='slug',
            field=models.SlugField(blank=True, max_length=250, help_text='URL-friendly version of name (auto-generated)'),
        ),
        migrations.AddField(
            model_name='committeemember',
            name='detailed_bio',
            field=models.TextField(blank=True, help_text='Detailed biography for bio page'),
        ),
        migrations.AddField(
            model_name='committeemember',
            name='research_interests',
            field=models.TextField(blank=True, help_text='Research interests (one per line)'),
        ),
        migrations.AddField(
            model_name='committeemember',
            name='publications',
            field=models.TextField(blank=True, help_text='Key publications'),
        ),
        migrations.AddField(
            model_name='committeemember',
            name='awards',
            field=models.TextField(blank=True, help_text='Awards and honors'),
        ),
        migrations.AddField(
            model_name='committeemember',
            name='education',
            field=models.TextField(blank=True, help_text='Educational background'),
        ),
        migrations.AddField(
            model_name='committeemember',
            name='website',
            field=models.URLField(blank=True, help_text='Personal/Professional website'),
        ),
        migrations.AddField(
            model_name='committeemember',
            name='linkedin',
            field=models.URLField(blank=True, help_text='LinkedIn profile URL'),
        ),
        migrations.AddField(
            model_name='committeemember',
            name='twitter',
            field=models.CharField(blank=True, max_length=100, help_text='Twitter handle (without @)'),
        ),
        migrations.AddField(
            model_name='committeemember',
            name='google_scholar',
            field=models.URLField(blank=True, help_text='Google Scholar profile URL'),
        ),
        migrations.AddField(
            model_name='committeemember',
            name='orcid',
            field=models.CharField(blank=True, max_length=100, help_text='ORCID ID'),
        ),
        migrations.AddField(
            model_name='committeemember',
            name='researchgate',
            field=models.URLField(blank=True, help_text='ResearchGate profile URL'),
        ),
        migrations.AddField(
            model_name='committeemember',
            name='enable_bio_page',
            field=models.BooleanField(default=True, help_text='Enable dedicated bio page'),
        ),
        migrations.AddField(
            model_name='committeemember',
            name='page_views',
            field=models.PositiveIntegerField(default=0, help_text='Number of bio page views'),
        ),
        migrations.AddField(
            model_name='committeemember',
            name='last_viewed',
            field=models.DateTimeField(blank=True, null=True, help_text='Last time bio page was viewed'),
        ),
        
        # Speaker fields
        migrations.AddField(
            model_name='speaker',
            name='slug',
            field=models.SlugField(blank=True, max_length=250, help_text='URL-friendly version of name (auto-generated)'),
        ),
        migrations.AddField(
            model_name='speaker',
            name='detailed_bio',
            field=models.TextField(blank=True, help_text='Detailed biography for bio page'),
        ),
        migrations.AddField(
            model_name='speaker',
            name='research_interests',
            field=models.TextField(blank=True, help_text='Research interests (one per line)'),
        ),
        migrations.AddField(
            model_name='speaker',
            name='publications',
            field=models.TextField(blank=True, help_text='Key publications'),
        ),
        migrations.AddField(
            model_name='speaker',
            name='awards',
            field=models.TextField(blank=True, help_text='Awards and honors'),
        ),
        migrations.AddField(
            model_name='speaker',
            name='education',
            field=models.TextField(blank=True, help_text='Educational background'),
        ),
        migrations.AddField(
            model_name='speaker',
            name='google_scholar',
            field=models.URLField(blank=True, help_text='Google Scholar profile URL'),
        ),
        migrations.AddField(
            model_name='speaker',
            name='researchgate',
            field=models.URLField(blank=True, help_text='ResearchGate profile URL'),
        ),
        migrations.AddField(
            model_name='speaker',
            name='enable_bio_page',
            field=models.BooleanField(default=True, help_text='Enable dedicated bio page'),
        ),
        migrations.AddField(
            model_name='speaker',
            name='page_views',
            field=models.PositiveIntegerField(default=0, help_text='Number of bio page views'),
        ),
        migrations.AddField(
            model_name='speaker',
            name='last_viewed',
            field=models.DateTimeField(blank=True, null=True, help_text='Last time bio page was viewed'),
        ),
        
        # Generate slugs for existing records
        migrations.RunPython(generate_slugs_committee, migrations.RunPython.noop),
        migrations.RunPython(generate_slugs_speaker, migrations.RunPython.noop),
        
        # Make slug unique after populating
        migrations.AlterField(
            model_name='committeemember',
            name='slug',
            field=models.SlugField(unique=True, blank=True, max_length=250, help_text='URL-friendly version of name (auto-generated)'),
        ),
        migrations.AlterField(
            model_name='speaker',
            name='slug',
            field=models.SlugField(unique=True, blank=True, max_length=250, help_text='URL-friendly version of name (auto-generated)'),
        ),
    ]
