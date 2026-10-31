"""Crawler-facing files: llms.txt, robots.txt and sitemap.xml.

Built from the same data the pages render (BENEFITS, FAQ_ITEMS, approved projects),
so they stay in sync without hand-editing.
"""
from xml.sax.saxutils import escape

from django.conf import settings
from django.http import HttpResponse
from django.urls import reverse
from django.views.decorators.http import require_GET

from dashboard.models import Builder, Project
from .views import BENEFITS, FAQ_ITEMS, LINKS

SUMMARY = (
    "Claude Builder Club (CBC) at Mizzou is a student-led community at the University of Missouri "
    "for learning, building, and shipping with Claude AI. It is a chapter of Anthropic's Campus "
    "Program, open to any currently enrolled Mizzou student of any major or coding experience."
)

# (url_name, title, description) for the llms.txt "Pages" section and the sitemap.
PAGES = [
    ('home', 'Home', 'Club overview and upcoming events calendar.'),
    ('about', 'About', 'Mission, spring hackathon, chapter stats, and FAQ.'),
    ('benefits', 'Member benefits', 'Claude Pro, API credits, hats and stickers, workshops.'),
    ('projects', 'Projects', 'Things members have built with Claude.'),
    ('team', 'Team', 'The current and past executive boards.'),
    ('gallery', 'Gallery', 'Photos from workshops, hackathons, and demo nights.'),
    ('connect', 'Connect', 'GroupMe, Instagram, LinkedIn, email, and member sign-up.'),
]


def _abs(path):
    return settings.SITE_URL.rstrip('/') + path


def _one_line(text):
    return ' '.join(text.split())


@require_GET
def llms_txt(request):
    lines = [
        '# Claude Builder Club @ Mizzou',
        '',
        f'> {SUMMARY}',
        '',
        '## Pages',
        '',
    ]
    for name, title, desc in PAGES:
        lines.append(f'- [{title}]({_abs(reverse(name))}): {desc}')

    lines += ['', '## Member benefits', '']
    for b in BENEFITS:
        lines.append(f"- {b['title']}: {b['description']}")

    lines += ['', '## FAQ', '']
    for item in FAQ_ITEMS:
        lines.append(f"- {item['question']} {item['answer']}")

    projects = Project.objects.approved()
    if projects:
        lines += ['', '## Projects', '']
        for p in projects:
            url = _abs(reverse('project_detail', args=[p.slug]))
            lines.append(f'- [{p.title}]({url}): {_one_line(p.description)}')

    lines += [
        '',
        '## Contact',
        '',
        f"- Sign up: {LINKS['signup']}",
        f"- GroupMe (fastest updates): {LINKS['groupme']}",
        f"- Instagram: {LINKS['instagram']}",
        f"- LinkedIn: {LINKS['linkedin']}",
        f"- Email: {LINKS['email'].removeprefix('mailto:')}",
        '',
        '## Optional',
        '',
        f"- [Claude]({LINKS['claude_ai']}): the AI assistant from Anthropic",
        f"- [Anthropic API docs]({LINKS['api_docs']}): documentation for building with Claude",
        '',
    ]
    return HttpResponse('\n'.join(lines), content_type='text/plain; charset=utf-8')


@require_GET
def robots_txt(request):
    body = '\n'.join([
        'User-agent: *',
        'Allow: /',
        'Disallow: /admin/',
        'Disallow: /cb-exec/',
        'Disallow: /submit-project/',
        '',
        f'Sitemap: {_abs(reverse("sitemap"))}',
        '',
    ])
    return HttpResponse(body, content_type='text/plain; charset=utf-8')


@require_GET
def sitemap_xml(request):
    entries = [(_abs(reverse(name)), None) for name, _, _ in PAGES]
    entries += [
        (_abs(reverse('project_detail', args=[p.slug])), p.updated_at)
        for p in Project.objects.approved()
    ]
    entries += [
        (_abs(reverse('builder_detail', args=[b.slug])), None)
        for b in Builder.objects.filter(is_approved=True)
    ]
    urls = []
    for loc, modified in entries:
        lastmod = f'<lastmod>{modified.date().isoformat()}</lastmod>' if modified else ''
        urls.append(f'  <url><loc>{escape(loc)}</loc>{lastmod}</url>')
    body = (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        + '\n'.join(urls) + '\n</urlset>\n'
    )
    return HttpResponse(body, content_type='application/xml')
