#!/usr/bin/env python
"""Script to create sample blog data for ICEIMS 2026 conference website."""

import os
import sys
import django

# Add the project directory to the Python path
project_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(project_dir)

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'iccca_website.settings')
django.setup()

from django.contrib.auth.models import User
from conference.models import Category, BlogPost
from django.utils import timezone

def create_sample_data():
    """Create sample categories, users, and blog posts."""
    
    print("🔧 Creating sample blog data for ICEIMS 2026...")
    
    # Create categories
    categories_data = [
        {
            'name': 'Conference News',
            'slug': 'conference-news',
            'description': 'Latest updates and announcements about ICEIMS 2026'
        },
        {
            'name': 'Research Insights',
            'slug': 'research-insights',
            'description': 'Academic research findings and scholarly discussions'
        },
        {
            'name': 'Technology Trends',
            'slug': 'technology-trends',
            'description': 'Emerging technologies and innovation updates'
        },
        {
            'name': 'Event Updates',
            'slug': 'event-updates',
            'description': 'Information about workshops, sessions, and networking events'
        }
    ]
    
    print("\n📁 Creating categories...")
    categories = {}
    for cat_data in categories_data:
        category, created = Category.objects.get_or_create(
            slug=cat_data['slug'],
            defaults={
                'name': cat_data['name'],
                'description': cat_data['description']
            }
        )
        categories[cat_data['slug']] = category
        status = "✅ Created" if created else "🔍 Found existing"
        print(f"   {status}: {category.name}")
    
    # Create admin user
    print("\n👤 Setting up admin user...")
    admin_user, created = User.objects.get_or_create(
        username='admin',
        defaults={
            'first_name': 'Conference',
            'last_name': 'Admin',
            'email': 'admin@iceims2026.com',
            'is_staff': True,
            'is_superuser': True
        }
    )
    
    if created:
        admin_user.set_password('admin123')
        admin_user.save()
        print("   ✅ Created admin user (username: admin, password: admin123)")
    else:
        print("   🔍 Found existing admin user")
    
    # Create sample blog posts
    print("\n📝 Creating sample blog posts...")
    
    blog_posts_data = [
        {
            'title': 'Welcome to ICEIMS 2026 Conference Blog',
            'slug': 'welcome-to-iceims-2026',
            'excerpt': 'We\'re excited to launch our official conference blog with the latest updates, insights, and announcements about ICEIMS 2026.',
            'content': '''
<p>Welcome to the official blog of the International Conference on Engineering, Information Management and Systems (ICEIMS 2026)!</p>

<p>This blog will serve as your go-to source for:</p>
<ul>
    <li>Conference updates and announcements</li>
    <li>Research insights from our speakers and participants</li>
    <li>Technology trends and innovations</li>
    <li>Event schedules and logistics</li>
    <li>Networking opportunities and community discussions</li>
</ul>

<p>We encourage all attendees, researchers, and industry professionals to engage with our content and share their insights. Stay tuned for exciting updates about keynote speakers, workshop sessions, and networking opportunities.</p>

<p>Don\'t forget to subscribe to our newsletter to receive the latest updates directly in your inbox!</p>
            ''',
            'category': 'conference-news',
            'featured': True
        },
        {
            'title': 'AI and Machine Learning: Shaping the Future of Engineering',
            'slug': 'ai-machine-learning-future-engineering',
            'excerpt': 'Explore how artificial intelligence and machine learning are revolutionizing engineering practices and creating new opportunities for innovation.',
            'content': '''
<p>Artificial Intelligence (AI) and Machine Learning (ML) are at the forefront of technological innovation, transforming how we approach engineering challenges and solutions.</p>

<h3>Key Applications in Engineering</h3>
<p>AI and ML are being integrated across various engineering disciplines:</p>
<ul>
    <li><strong>Predictive Maintenance:</strong> Using ML algorithms to predict equipment failures before they occur</li>
    <li><strong>Design Optimization:</strong> AI-driven design tools that optimize performance and efficiency</li>
    <li><strong>Quality Control:</strong> Computer vision systems for automated quality inspection</li>
    <li><strong>Process Automation:</strong> Intelligent systems that adapt to changing conditions</li>
</ul>

<h3>Future Implications</h3>
<p>As we look toward the future, the integration of AI and ML in engineering will continue to accelerate, bringing both opportunities and challenges that our conference will address.</p>

<p>Join us at ICEIMS 2026 to explore these exciting developments!</p>
            ''',
            'category': 'technology-trends',
            'featured': True
        },
        {
            'title': 'Call for Papers: ICEIMS 2026 Research Track',
            'slug': 'call-for-papers-research-track',
            'excerpt': 'Submit your groundbreaking research to ICEIMS 2026. We\'re accepting papers across multiple engineering and information systems domains.',
            'content': '''
<p>We invite researchers, academics, and industry professionals to submit their original research papers to ICEIMS 2026.</p>

<h3>Research Areas</h3>
<p>We welcome submissions in the following areas:</p>
<ul>
    <li>Artificial Intelligence and Machine Learning</li>
    <li>Internet of Things (IoT) and Smart Systems</li>
    <li>Cybersecurity and Information Security</li>
    <li>Sustainable Engineering Solutions</li>
    <li>Data Analytics and Big Data</li>
    <li>Blockchain and Distributed Systems</li>
    <li>Human-Computer Interaction</li>
    <li>Software Engineering and Systems</li>
</ul>

<h3>Important Dates</h3>
<ul>
    <li><strong>Abstract Submission:</strong> March 15, 2026</li>
    <li><strong>Full Paper Submission:</strong> April 30, 2026</li>
    <li><strong>Review Notification:</strong> June 15, 2026</li>
    <li><strong>Camera-Ready Submission:</strong> July 31, 2026</li>
</ul>

<p>For detailed submission guidelines, please visit our submission guidelines page.</p>
            ''',
            'category': 'conference-news',
            'featured': False
        },
        {
            'title': 'Keynote Speaker Announcement: Dr. Sarah Chen',
            'slug': 'keynote-speaker-dr-sarah-chen',
            'excerpt': 'We\'re thrilled to announce Dr. Sarah Chen as our opening keynote speaker for ICEIMS 2026, discussing the future of sustainable engineering.',
            'content': '''
<p>We are honored to announce that <strong>Dr. Sarah Chen</strong>, renowned expert in sustainable engineering and green technology, will deliver the opening keynote address at ICEIMS 2026.</p>

<h3>About Dr. Chen</h3>
<p>Dr. Chen is a Professor of Environmental Engineering at Stanford University and has over 20 years of experience in sustainable technology development. Her research focuses on:</p>
<ul>
    <li>Renewable energy systems</li>
    <li>Carbon capture technologies</li>
    <li>Sustainable manufacturing processes</li>
    <li>Environmental impact assessment</li>
</ul>

<h3>Keynote Topic</h3>
<p><em>"Engineering for a Sustainable Future: Bridging Innovation and Environmental Responsibility"</em></p>

<p>Dr. Chen will explore how engineering innovation can drive environmental sustainability while maintaining economic viability. She will share insights from her latest research and discuss emerging trends in green technology.</p>

<p>Don\'t miss this inspiring presentation that will set the tone for our conference discussions on sustainable engineering solutions!</p>
            ''',
            'category': 'event-updates',
            'featured': True
        },
        {
            'title': 'Workshop Registration Now Open: Hands-on IoT Development',
            'slug': 'workshop-iot-development',
            'excerpt': 'Join our hands-on workshop on IoT development using cutting-edge platforms and tools. Limited seats available!',
            'content': '''
<p>We\'re excited to announce that registration is now open for our hands-on IoT Development Workshop at ICEIMS 2026!</p>

<h3>Workshop Details</h3>
<ul>
    <li><strong>Duration:</strong> 4 hours (with breaks)</li>
    <li><strong>Level:</strong> Intermediate to Advanced</li>
    <li><strong>Max Participants:</strong> 30</li>
    <li><strong>Prerequisites:</strong> Basic programming knowledge</li>
</ul>

<h3>What You\'ll Learn</h3>
<ul>
    <li>IoT architecture and design principles</li>
    <li>Sensor integration and data collection</li>
    <li>Cloud connectivity and data analytics</li>
    <li>Security considerations for IoT systems</li>
</ul>

<p>All materials and hardware will be provided. Register early as seats are limited!</p>
            ''',
            'category': 'event-updates',
            'featured': False
        }
    ]
    
    for post_data in blog_posts_data:
        category = categories[post_data['category']]
        post, created = BlogPost.objects.get_or_create(
            slug=post_data['slug'],
            defaults={
                'title': post_data['title'],
                'excerpt': post_data['excerpt'],
                'content': post_data['content'],
                'author': admin_user,
                'category': category,
                'status': 'published',
                'featured': post_data['featured'],
                'published_at': timezone.now()
            }
        )
        status = "✅ Created" if created else "🔍 Found existing"
        print(f"   {status}: {post.title}")
    
    # Print summary
    print(f"\n📊 Summary:")
    print(f"   Total categories: {Category.objects.count()}")
    print(f"   Total blog posts: {BlogPost.objects.count()}")
    print(f"   Published posts: {BlogPost.objects.filter(status='published').count()}")
    print(f"   Featured posts: {BlogPost.objects.filter(featured=True).count()}")
    
    print(f"\n🎉 Sample blog data created successfully!")
    print(f"\n📋 Admin Login Details:")
    print(f"   Username: admin")
    print(f"   Password: admin123")
    print(f"   Access: http://localhost:8000/admin/blog/ (for blog management)")
    print(f"   Public Blog: http://localhost:8000/blog/ (for public viewing)")

if __name__ == '__main__':
    create_sample_data()