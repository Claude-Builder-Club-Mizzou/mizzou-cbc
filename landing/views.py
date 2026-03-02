from django.shortcuts import render
from dashboard.models import GalleryImage, Event, Project


def index(request):
    # Database-backed content
    gallery_images = GalleryImage.objects.all()
    events = [e.to_template_dict() for e in Event.objects.all()]
    projects = Project.objects.all()

    context = {
        'benefits': [
            {
                'icon': '🚀',
                'title': 'Claude Pro Access',
                'description': 'Free unlimited access to Claude\'s most advanced models with priority processing. Build, research, and create without limits.',
            },
            {
                'icon': '💻',
                'title': '$50/mo API Credits',
                'description': 'Monthly API credits to build real applications powered by Claude. Ship projects, automate workflows, and experiment freely.',
            },
            {
                'icon': '🎓',
                'title': 'Workshops & Hackathons',
                'description': 'Hands-on workshops, weekend hackathons, and demo nights. Learn prompt engineering, AI app development, and more.',
            },
            {
                'icon': '🤝',
                'title': 'Community & Networking',
                'description': 'Connect with fellow builders across all majors. Guest speakers from Anthropic and industry leaders share insights.',
            },
        ],
        'gallery': gallery_images,
        'events': events,
        'stats': [
            {'value': '60+', 'num': 60, 'label': 'Universities Nationwide'},
            {'value': '15K+', 'num': 15000, 'label': 'Student Builders'},
            {'value': '7', 'num': 7, 'label': 'Ivy League Schools'},
            {'value': '∞', 'num': 0, 'label': 'Projects to Build'},
        ],
        'team': [
            {'name': 'Brandon Gomes', 'initials': 'BG', 'role': 'President', 'major': 'BS in Computer Science & Math, Senior', 'linkedin': 'https://www.linkedin.com/in/brandon-gomes-mu/', 'image': 'landing/images/team/brandon.jpeg'},
            {'name': 'Pari Patel', 'initials': 'PP', 'role': 'Vice President', 'major': 'BS in Computer Science, Senior', 'linkedin': 'https://www.linkedin.com/in/paripatel54/', 'image': 'landing/images/team/pari.jpeg'},
            {'name': 'Colton Treloar', 'initials': 'CT', 'role': 'Treasurer', 'major': 'Computer Science, Junior', 'linkedin': 'https://www.linkedin.com/in/colton-treloar-613442206/', 'image': 'landing/images/team/colton.jpg'},
            {'name': 'Akbar K.', 'initials': 'AK', 'role': 'Secretary', 'major': 'BS in Electrical Engineering, Junior', 'linkedin': 'https://www.linkedin.com/in/akbarjon-kamoldinov/', 'image': 'landing/images/team/akbar.jpeg'},
            {'name': 'Sebastian Main', 'initials': 'SM', 'role': 'Outreach', 'major': 'Information Technology, Junior', 'linkedin': 'https://www.linkedin.com/in/sebastian-main-6a4799224/', 'image': 'landing/images/team/sebastian.jpg'},
        ],
        'projects': projects,
        'faq_items': [
            {
                'question': 'Who can join CBC Mizzou?',
                'answer': 'Any currently enrolled Mizzou student can join, regardless of major or coding experience. We welcome engineers, journalists, business students, artists — anyone interested in building with AI.',
            },
            {
                'question': 'Do I need coding experience?',
                'answer': "Not at all! We have tracks for all skill levels. Our workshops start from the basics, and Claude itself is a great tool for learning to code. Many of our most creative projects come from non-CS majors.",
            },
            {
                'question': 'How do I get free Claude Pro access?',
                'answer': "Join the club by filling out our sign-up form. Once you're a member, you'll receive instructions to activate your free Claude Pro subscription within a few days.",
            },
            {
                'question': "What's the time commitment?",
                'answer': "Totally flexible. We host events 2-3 times per month, and attendance is optional. Come to what interests you — whether that's every workshop or just the hackathons.",
            },
            {
                'question': 'How are the $50 monthly API credits distributed?',
                'answer': "Active members receive API credits through Anthropic's program. You'll get access to the Claude API to build personal projects, class assignments, or hackathon submissions.",
            },
            {
                'question': 'Can I join the leadership team?',
                'answer': "Yes! We're always looking for motivated students to help lead workshops, organize events, manage social media, and grow the community. Reach out to any current leader to learn more.",
            },
            {
                'question': 'Where do meetings take place?',
                'answer': 'We rotate between rooms in Lafferre Hall, the Engineering Building, and the Student Center. Check our GroupMe and events calendar for specific locations each week.',
            },
        ],
        'links': {
            'groupme': 'https://groupme.com/join_group/112902855/DrXZJmkl',
            'instagram': 'https://www.instagram.com/claude.miz/',
            'linkedin': 'https://www.linkedin.com/groups/18313009/',
            'email': 'mailto:cbcmizzou@gmail.com',
            'signup': 'https://forms.gle/K6WxeEaavtafNjAP7',
            'claude_ai': 'https://claude.ai',
            'anthropic': 'https://anthropic.com',
            'api_docs': 'https://docs.anthropic.com',
        },
    }
    return render(request, 'landing/index.html', context)