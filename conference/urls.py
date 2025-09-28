from django.urls import path
from . import views

app_name = 'conference'

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('tracks/', views.tracks, name='tracks'),
    path('committee/members/', views.committee, name='committee'),
    path('committee/speakers/', views.keynotes, name='speakers'),
    path('attractions/', views.attractions, name='attractions'),
    path('contact/', views.contact, name='contact'),
    path('guidelines/', views.guidelines, name='guidelines'),
    path('registration/', views.registration, name='registration'),
    path('workshops/', views.workshops, name='workshops'),
    path('panels/', views.panels, name='panels'),
    path('networking/', views.networking, name='networking'),
    path('previous/', views.previous, name='previous'),
    path('schedule/', views.schedule, name='schedule'),
    path('awards/', views.awards, name='awards'),
    path('sponsors/', views.sponsors, name='sponsors'),
    # Hidden test page - not linked in navigation
    path('secret-animations-test/', views.animations_test, name='animations_test'),
]