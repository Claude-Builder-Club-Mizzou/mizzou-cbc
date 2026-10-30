from django.shortcuts import render
from dashboard.models import GalleryImage, Event, Project, TeamMember

NAV_ITEMS = [
    {'url_name': 'home', 'label': 'Home'},
    {'url_name': 'about', 'label': 'About'},
    {'url_name': 'gallery', 'label': 'Gallery'},
    {'url_name': 'benefits', 'label': 'Benefits'},
    {'url_name': 'team', 'label': 'Team'},
    {'url_name': 'projects', 'label': 'Projects'},
    {'url_name': 'connect', 'label': 'Connect'},
]

LINKS = {
    'groupme': 'https://groupme.com/join_group/112902855/DrXZJmkl',
    'instagram': 'https://www.instagram.com/claude.miz/',
    'linkedin': 'https://www.linkedin.com/groups/18313009/',
    'email': 'mailto:cbcmizzou@gmail.com',
    'signup': 'https://www.jotform.com/253555944387168',
    'claude_ai': 'https://claude.ai',
    'anthropic': 'https://anthropic.com',
    'api_docs': 'https://docs.anthropic.com',
}

BENEFITS = [
    {
        'icon': '<svg width="40" height="40" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M13 2L3 14h9l-1 8 10-12h-9l1-8z" stroke="#D97757" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>',
        'title': 'Merchandise',
        'description': 'Earn Claude Builder Club merchandise, including stickers and apparel, through club activities, events, and projects.',
    },
    {
        'icon': '<svg width="40" height="40" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M16 18l2-2-2-2M8 18l-2-2 2-2M14 4l-4 16" stroke="#D97757" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>',
        'title': 'Claude Pro & API Credits',
        'description': 'Members get 3 months of Claude Pro free, plus $25 in API credits each fall and $50 each spring to build real applications powered by Claude. Ship projects, automate workflows, and experiment freely.',
    },
    {
        'icon': '<svg width="40" height="40" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M22 10v6M2 10l10-5 10 5-10 5-10-5z" stroke="#D97757" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/><path d="M6 12v5c0 1.66 2.69 3 6 3s6-1.34 6-3v-5" stroke="#D97757" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>',
        'title': 'Workshops & Hackathons',
        'description': 'Hands-on workshops, weekend hackathons, and demo nights. Learn prompt engineering, AI app development, and more.',
    },
    {
        'icon': '<svg width="40" height="40" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M17 21v-2a4 4 0 00-4-4H5a4 4 0 00-4 4v2M9 11a4 4 0 100-8 4 4 0 000 8zM23 21v-2a4 4 0 00-3-3.87M16 3.13a4 4 0 010 7.75" stroke="#D97757" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>',
        'title': 'Community & Networking',
        'description': 'Connect with fellow builders across all majors. Guest speakers from Anthropic and industry leaders share insights.',
    },
]

STATS = [
    {'value': '60+', 'num': 60, 'label': 'Universities Nationwide'},
    {'value': '15K+', 'num': 15000, 'label': 'Student Builders'},
    {'value': '7', 'num': 7, 'label': 'Ivy League Schools'},
    {'value': '∞', 'num': 0, 'label': 'Projects to Build'},
]

FAQ_ITEMS = [
    {
        'question': 'Who can join CBC Mizzou?',
        'answer': 'Any currently enrolled Mizzou student can join, regardless of major or coding experience. We welcome engineers, journalists, business students, artists — anyone interested in building with AI.',
    },
    {
        'question': 'Do I need coding experience?',
        'answer': "Not at all! We have tracks for all skill levels. Our workshops start from the basics, and Claude itself is a great tool for learning to code. Many of our most creative projects come from non-CS majors.",
    },
    {
        'question': 'How do I get merchandise?',
        'answer': "Join the club by filling out our sign-up form. Once you're a member, you'll be eligible for merchandise opportunities through club events and activities. Check our GroupMe for details.",
    },
    {
        'question': "What's the time commitment?",
        'answer': "Totally flexible. We host events 2-3 times per month, and attendance is optional. Come to what interests you — whether that's every workshop or just the hackathons.",
    },
    {
        'question': 'How are the API credits distributed?',
        'answer': "Active members receive $25 in API credits in the fall and $50 in the spring through Anthropic's program. You'll get access to the Claude API to build personal projects, class assignments, or hackathon submissions.",
    },
    {
        'question': 'Can I join the leadership team?',
        'answer': "Yes! We're always looking for motivated students to help lead workshops, organize events, manage social media, and grow the community. Reach out to any current leader to learn more.",
    },
    {
        'question': 'Where do meetings take place?',
        'answer': 'We rotate between rooms in Lafferre Hall, the Engineering Building, and the Student Center. Check our GroupMe and events calendar for specific locations each week.',
    },
]


def _render(request, template, page, **context):
    """Render a landing page with the context every page needs (nav + shared links)."""
    context.update({'nav_items': NAV_ITEMS, 'current_page': page, 'links': LINKS})
    return render(request, template, context)


def home(request):
    events = [e.to_template_dict() for e in Event.objects.all()]
    return _render(request, 'landing/home.html', 'home', events=events)


def about(request):
    return _render(request, 'landing/about.html', 'about', stats=STATS, faq_items=FAQ_ITEMS)


def gallery(request):
    return _render(request, 'landing/gallery.html', 'gallery', gallery=GalleryImage.objects.all())


def benefits(request):
    return _render(request, 'landing/benefits.html', 'benefits', benefits=BENEFITS)


def team(request):
    return _render(request, 'landing/team.html', 'team', team=TeamMember.objects.all())


def projects(request):
    return _render(request, 'landing/projects.html', 'projects', projects=Project.objects.all())


def connect(request):
    return _render(request, 'landing/connect.html', 'connect')
