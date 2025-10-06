"""
Debug views for media files
"""
from django.http import JsonResponse, HttpResponse
from django.conf import settings
from django.contrib.admin.views.decorators import staff_member_required
from conference.models import Sponsor, CommitteeMember, TouristAttraction, HeroSlide, SiteSettings
import os


@staff_member_required
def media_debug(request):
    """
    Debug view to check media file status
    """
    
    data = {
        'media_root': str(settings.MEDIA_ROOT),
        'media_url': settings.MEDIA_URL,
        'debug': settings.DEBUG,
        'media_root_exists': os.path.exists(settings.MEDIA_ROOT),
        'issues': [],
        'stats': {}
    }
    
    # Check sponsors
    sponsors = Sponsor.objects.filter(logo__isnull=False).exclude(logo='')
    sponsor_issues = []
    for sponsor in sponsors:
        if sponsor.logo:
            exists = os.path.exists(sponsor.logo.path) if hasattr(sponsor.logo, 'path') else False
            if not exists:
                sponsor_issues.append({
                    'name': sponsor.name,
                    'path': str(sponsor.logo),
                    'exists': exists
                })
    
    data['stats']['sponsors_total'] = sponsors.count()
    data['stats']['sponsors_missing'] = len(sponsor_issues)
    if sponsor_issues:
        data['issues'].extend([f"Sponsor '{s['name']}': {s['path']}" for s in sponsor_issues])
    
    # Check committee members
    members = CommitteeMember.objects.filter(image__isnull=False).exclude(image='')
    member_issues = []
    for member in members:
        if member.image:
            exists = os.path.exists(member.image.path) if hasattr(member.image, 'path') else False
            if not exists:
                member_issues.append({
                    'name': member.name,
                    'path': str(member.image),
                    'exists': exists
                })
    
    data['stats']['members_total'] = members.count()
    data['stats']['members_missing'] = len(member_issues)
    if member_issues:
        data['issues'].extend([f"Member '{m['name']}': {m['path']}" for m in member_issues])
    
    # Check hero slides
    slides = HeroSlide.objects.filter(image__isnull=False).exclude(image='')
    slide_issues = []
    for slide in slides:
        if slide.image:
            exists = os.path.exists(slide.image.path) if hasattr(slide.image, 'path') else False
            if not exists:
                slide_issues.append({
                    'title': slide.title or f'Slide {slide.id}',
                    'path': str(slide.image),
                    'exists': exists
                })
    
    data['stats']['slides_total'] = slides.count()
    data['stats']['slides_missing'] = len(slide_issues)
    if slide_issues:
        data['issues'].extend([f"Slide '{s['title']}': {s['path']}" for s in slide_issues])
    
    # List media directory contents
    if os.path.exists(settings.MEDIA_ROOT):
        data['media_directories'] = {}
        for item in os.listdir(settings.MEDIA_ROOT):
            item_path = os.path.join(settings.MEDIA_ROOT, item)
            if os.path.isdir(item_path):
                file_count = len([f for f in os.listdir(item_path) if os.path.isfile(os.path.join(item_path, f))])
                data['media_directories'][item] = file_count
    
    # Summary
    data['summary'] = {
        'total_issues': len(data['issues']),
        'status': 'OK' if len(data['issues']) == 0 else 'ISSUES FOUND'
    }
    
    # Return as JSON
    if request.GET.get('format') == 'json':
        return JsonResponse(data, json_dumps_params={'indent': 2})
    
    # Return as HTML
    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Media Files Debug</title>
        <style>
            body {{ font-family: monospace; padding: 20px; background: #f5f5f5; }}
            .container {{ max-width: 1200px; margin: 0 auto; background: white; padding: 20px; border-radius: 8px; }}
            h1 {{ color: #333; }}
            .status {{ padding: 10px; margin: 10px 0; border-radius: 4px; }}
            .status.ok {{ background: #d4edda; color: #155724; }}
            .status.error {{ background: #f8d7da; color: #721c24; }}
            .info {{ background: #e7f3ff; padding: 10px; margin: 10px 0; border-left: 4px solid #2196F3; }}
            .issue {{ background: #fff3cd; padding: 10px; margin: 5px 0; border-left: 4px solid #ff9800; }}
            pre {{ background: #f4f4f4; padding: 10px; overflow-x: auto; }}
            table {{ width: 100%; border-collapse: collapse; margin: 10px 0; }}
            th, td {{ padding: 8px; text-align: left; border-bottom: 1px solid #ddd; }}
            th {{ background: #f4f4f4; }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>📁 Media Files Debug Information</h1>
            
            <div class="status {'ok' if data['summary']['total_issues'] == 0 else 'error'}">
                <strong>Status:</strong> {data['summary']['status']} ({data['summary']['total_issues']} issues)
            </div>
            
            <h2>Configuration</h2>
            <div class="info">
                <strong>MEDIA_ROOT:</strong> {data['media_root']}<br>
                <strong>MEDIA_URL:</strong> {data['media_url']}<br>
                <strong>DEBUG:</strong> {data['debug']}<br>
                <strong>Media root exists:</strong> {data['media_root_exists']}
            </div>
            
            <h2>Statistics</h2>
            <table>
                <tr>
                    <th>Model</th>
                    <th>Total</th>
                    <th>Missing</th>
                </tr>
                <tr>
                    <td>Sponsors</td>
                    <td>{data['stats'].get('sponsors_total', 0)}</td>
                    <td>{data['stats'].get('sponsors_missing', 0)}</td>
                </tr>
                <tr>
                    <td>Committee Members</td>
                    <td>{data['stats'].get('members_total', 0)}</td>
                    <td>{data['stats'].get('members_missing', 0)}</td>
                </tr>
                <tr>
                    <td>Hero Slides</td>
                    <td>{data['stats'].get('slides_total', 0)}</td>
                    <td>{data['stats'].get('slides_missing', 0)}</td>
                </tr>
            </table>
            
            <h2>Media Directories</h2>
            <table>
                <tr>
                    <th>Directory</th>
                    <th>Files</th>
                </tr>
                {''.join([f"<tr><td>{k}/</td><td>{v}</td></tr>" for k, v in data.get('media_directories', {}).items()])}
            </table>
            
            <h2>Issues ({len(data['issues'])})</h2>
            {''.join([f"<div class='issue'>{issue}</div>" for issue in data['issues']]) if data['issues'] else '<p>No issues found!</p>'}
            
            <hr>
            <p><a href="?format=json">View as JSON</a> | <a href="/admin-panel/">Back to Admin</a></p>
        </div>
    </body>
    </html>
    """
    
    return HttpResponse(html)
