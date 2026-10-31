from collections import defaultdict

from django.shortcuts import render
from django.templatetags.static import static
from dashboard.models import GalleryImage, Event, Project, TeamMember
from dashboard.terms import all_terms, current_term, term_label, term_status

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
        'icon': '<svg width="40" height="40" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M11.562 3.266a.5.5 0 0 1 .876 0L15.39 8.87a1 1 0 0 0 1.516.294L21.183 5.5a.5.5 0 0 1 .798.519l-2.834 10.246a1 1 0 0 1-.956.734H5.81a1 1 0 0 1-.957-.734L2.02 6.02a.5.5 0 0 1 .798-.519l4.276 3.664a1 1 0 0 0 1.516-.294z" fill="#D97757" stroke="#D97757" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/><path d="M5 21h14" stroke="#D97757" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>',
        'title': '3 Months of Claude Pro',
        'description': 'Members get 3 months of Claude Pro free, so you can write, research, and code with Claude every day.',
    },
    {
        'icon': '<img src="' + static('landing/images/icons/claude-code-guy.svg') + '" alt="">',
        'title': '$25 in API Credits',
        'description': 'Get $25 in API credits each fall ($50 each spring) to build real applications, automate workflows, and experiment freely.',
    },
    {
        'icon': '<img src="' + static('landing/images/icons/claude-logo.svg') + '" alt="">',
        'title': 'Merchandise',
        'description': 'Earn stickers and hats through club activities, events, and projects.',
    },
    {
        'icon': '<svg width="40" height="40" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><circle cx="9" cy="7" r="4" fill="#D97757" stroke="#D97757" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/><path d="M2 21v-2a4 4 0 014-4h6a4 4 0 014 4v2z" fill="#D97757" stroke="#D97757" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/><circle cx="17.5" cy="7.5" r="2.5" fill="#D97757" stroke="#D97757" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/><path d="M17 14.5a4 4 0 016 3.5v3h-4" fill="#D97757" stroke="#D97757" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>',
        'title': 'Community, Workshops & Hackathons',
        'description': 'Hands-on workshops, weekend hackathons, and demo nights, plus guest speakers from Anthropic and industry. Connect with builders across all majors.',
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
    by_term = defaultdict(list)
    for member in TeamMember.objects.all():
        by_term[member.term].append(member)

    # Past boards only, newest first; upcoming boards stay hidden until they take office.
    past_boards = [
        {'key': key, 'label': label, 'members': by_term[key]}
        for key, label in reversed(all_terms())
        if term_status(key) == 'past' and by_term.get(key)
    ]
    current = current_term()
    return _render(
        request, 'landing/team.html', 'team',
        current_board={'key': current, 'label': term_label(current), 'members': by_term.get(current, [])},
        past_boards=past_boards,
    )


def projects(request):
    return _render(request, 'landing/projects.html', 'projects', projects=Project.objects.all())


def connect(request):
    return _render(request, 'landing/connect.html', 'connect')
