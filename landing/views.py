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
        'title': 'API Credits Every Semester',
        'description': 'Get $25 in API credits in the fall and $50 in the spring to build real applications, automate workflows, and experiment freely.',
    },
    {
        'icon': '<img src="' + static('landing/images/icons/claude-logo.svg') + '" alt="">',
        'title': 'Hats & Stickers',
        'description': 'Members get Claude hats and stickers on top of everything else.',
        'merch': [
            {'src': static('landing/images/claude-hat.png'), 'label': 'Hat'},
            {'src': static('landing/images/claude-sticker.png'), 'label': 'Sticker'},
            {'src': static('landing/images/claude-eyes.png'), 'label': 'Sticker'},
            {'src': static('landing/images/claude-coffe.png'), 'label': 'Sticker'},
        ],
    },
    {
        'icon': '<svg width="40" height="40" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><circle cx="9" cy="7" r="4" fill="#D97757" stroke="#D97757" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/><path d="M2 21v-2a4 4 0 014-4h6a4 4 0 014 4v2z" fill="#D97757" stroke="#D97757" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/><circle cx="17.5" cy="7.5" r="2.5" fill="#D97757" stroke="#D97757" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/><path d="M17 14.5a4 4 0 016 3.5v3h-4" fill="#D97757" stroke="#D97757" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>',
        'title': 'Community, Workshops & Hackathons',
        'description': 'Hands-on workshops, weekend hackathons, and demo nights, plus guest speakers from Anthropic and industry. Connect with builders across all majors.',
    },
]

STATS = [
    {'value': '82', 'num': 82, 'label': 'Schools Worldwide'},
    {'value': '15K+', 'num': 15000, 'label': 'Student Builders'},
    {'value': '8', 'num': 8, 'label': 'Countries & Regions'},
    {'value': '∞', 'num': 0, 'label': 'Projects to Build'},
]

FAQ_ITEMS = [
    {
        'question': 'Who can join CBC Mizzou?',
        'answer': "Any currently enrolled Mizzou student can join, whether you're an undergrad or a grad student and whatever your major or coding experience. Engineers, journalists, business students, and artists are all welcome. If you're curious about building with AI, you're in.",
    },
    {
        'question': 'Do I need coding experience?',
        'answer': "No. Our workshops start with Claude itself, then move to Claude Code and the Claude API, so you can begin with a simple prompt and go as far as you want. Claude is also a good way to learn to code.",
    },
    {
        'question': 'What do members get?',
        'answer': "Through Anthropic's Campus Program, members get 3 months of Claude Pro, API credits, and Claude hats and stickers, along with workshops, hackathons, and demo nights. Sign up with the form on this site, then watch our GroupMe for how and when perks are handed out.",
    },
    {
        'question': "What's the time commitment?",
        'answer': "As much or as little as you want. Come to the workshops that interest you, the hackathon, or just a demo night to see what others are building. Check our upcoming events on the homepage calendar.",
    },
    {
        'question': 'How do the API credits work?',
        'answer': "Members receive $25 in API credits in the fall and $50 in the spring. Use them for personal projects, class assignments, or hackathon entries. Credit amounts can change from term to term, so check the GroupMe for the latest.",
    },
    {
        'question': 'Is there a hackathon?',
        'answer': "Yes. We host one every spring. Teams spend a weekend building with Claude, and the best projects win API credits. Dates and details go out on our GroupMe and the events page once they're confirmed.",
    },
    {
        'question': 'Can I join the leadership team?',
        'answer': "Yes. We're always looking for students who want to help run workshops, plan events, manage social media, and grow the community. Message any current board member or email us to learn more.",
    },
    {
        'question': 'Where and when are meetings?',
        'answer': 'Locations and times change by event, so the events page and our GroupMe always have the current details.',
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
