from django.shortcuts import render
from django.http import HttpResponse
from .models import (
    CommitteeMember, ConferenceTrack, TouristAttraction, 
    ImportantDate, Slider, ConferenceSettings, Sponsor
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
