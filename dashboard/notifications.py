import logging

from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.urls import reverse

logger = logging.getLogger(__name__)


def _absolute(path):
    """Full URL for a site path or media URL, built from SITE_URL so links are right behind a proxy."""
    if not path:
        return ''
    if path.startswith(('http://', 'https://')):
        return path
    return settings.SITE_URL.rstrip('/') + path


def notify_new_submission(project, builder):
    """Email the exec inbox about a new project submission (HTML with a plain-text fallback).

    Never raises: a mail outage must not lose or block a submission,
    since it is already saved and waiting in the dashboard.
    """
    title = ' '.join(project.title.split())  # no newlines in a header
    context = {
        'project': project,
        'builder': builder,
        'cover_url': _absolute(project.image.url) if project.image else '',
        'review_url': _absolute(reverse('dashboard:submissions')),
    }
    try:
        message = EmailMultiAlternatives(
            subject=f"New project submission: {title}"[:150],
            body=render_to_string('dashboard/email/new_submission.txt', context),
            to=[settings.SUBMISSION_NOTIFY_EMAIL],
            reply_to=[builder.email] if builder.email else None,
        )
        message.attach_alternative(render_to_string('dashboard/email/new_submission.html', context), 'text/html')
        message.send()
        return True
    except Exception:
        logger.exception('Could not send the new-submission email for project %s', project.pk)
        return False
