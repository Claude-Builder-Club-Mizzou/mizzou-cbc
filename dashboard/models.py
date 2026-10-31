from urllib.parse import parse_qs, urlparse

from django.db import models
from django.utils.text import slugify
from django.templatetags.static import static

from .terms import current_term_key, term_label


class GalleryImage(models.Model):
    caption = models.CharField(max_length=200)
    image = models.ImageField(upload_to='gallery/')
    order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['order', '-created_at']

    def __str__(self):
        return self.caption


class Event(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    location = models.CharField(max_length=200)
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    rsvp_url = models.URLField(blank=True, default='', help_text='Campus RSVP link (optional)')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['date', 'start_time']

    def __str__(self):
        return f"{self.title} ({self.date})"

    def _format_time(self, t):
        """Format time as '2:00 PM' — works on both Windows and Unix."""
        return t.strftime('%I:%M %p').lstrip('0')

    def to_template_dict(self):
        """Format event data the way landing/home.html expects it."""
        return {
            'id': self.pk,
            'rsvp_url': self.rsvp_url,
            'weekday': self.date.strftime('%a'),
            'month': self.date.strftime('%b'),
            'day': str(self.date.day),
            'year': self.date.year,
            'month_num': self.date.month,
            'day_num': self.date.day,
            'title': self.title,
            'description': self.description,
            'location': self.location,
            'time': f"{self._format_time(self.start_time)} – {self._format_time(self.end_time)}",
        }


def _unique_slug(model, text, instance_pk=None, fallback='item'):
    """Slugify `text`, appending -2, -3... until no other row of `model` uses it."""
    base = slugify(text)[:50] or fallback
    slug, n = base, 2
    qs = model.objects.exclude(pk=instance_pk) if instance_pk else model.objects.all()
    while qs.filter(slug=slug).exists():
        slug = f"{base}-{n}"
        n += 1
    return slug


class Builder(models.Model):
    """A club member who builds projects (separate from the exec-board TeamMember)."""
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=60, unique=True, blank=True, editable=False)
    major = models.CharField(max_length=200, blank=True, help_text='e.g. Computer Science')
    year = models.CharField(max_length=50, blank=True, help_text='e.g. Junior, Grad Student')
    bio = models.TextField(blank=True)
    photo = models.ImageField(upload_to='builders/', blank=True)
    linkedin = models.URLField(blank=True, default='')
    github = models.URLField(blank=True, default='')
    website = models.URLField(blank=True, default='')
    email = models.EmailField(blank=True, default='',
                              help_text='Private contact address from a submission. Never shown on the site.')
    is_approved = models.BooleanField(default=True,
                                      help_text='Unapproved profiles (from submissions) are hidden from the public site')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = _unique_slug(Builder, self.name, self.pk, 'builder')
        super().save(*args, **kwargs)

    @property
    def initials(self):
        parts = self.name.replace('.', ' ').split()
        if not parts:
            return '?'
        if len(parts) == 1:
            return parts[0][0].upper()
        return (parts[0][0] + parts[-1][0]).upper()

    @property
    def subtitle(self):
        return ', '.join(x for x in (self.major, self.year) if x)


class ProjectQuerySet(models.QuerySet):
    def approved(self):
        return self.filter(status=Project.APPROVED)

    def pending(self):
        return self.filter(status=Project.PENDING)


class Project(models.Model):
    PENDING, APPROVED, REJECTED = 'pending', 'approved', 'rejected'
    STATUS_CHOICES = [(PENDING, 'Pending review'), (APPROVED, 'Approved'), (REJECTED, 'Rejected')]

    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=60, unique=True, blank=True, editable=False)
    description = models.TextField(help_text='Short summary shown on the project card')
    image = models.ImageField(upload_to='projects/', blank=True, help_text='Cover image')
    tech = models.JSONField(default=list, help_text='List of tech tags, e.g. ["Next.js", "Supabase"]')
    builders = models.ManyToManyField(Builder, blank=True, related_name='projects')

    # Detail page content
    story = models.TextField(blank=True, help_text='The full write-up: what it is, why it exists, how it works')
    claude_usage = models.TextField(blank=True, help_text='How Claude was used to build or power this project')
    challenges = models.TextField(blank=True, help_text='What was hard, and what was learned')

    # Links
    link = models.URLField(blank=True, default='', help_text='Live site / app')
    github_url = models.URLField(blank=True, default='')
    demo_video_url = models.URLField(blank=True, default='', help_text='YouTube, Loom, or a direct video link')

    built_at = models.CharField(max_length=120, blank=True, help_text='Where it was built, e.g. Spring 2026 Hackathon, Demo Night, ENGR 1100')
    coming_soon = models.BooleanField(default=False)
    featured = models.BooleanField(default=False, help_text='Pin to the top of the projects page')
    order = models.PositiveIntegerField(default=0)
    # Projects added in the dashboard are live right away; member submissions start as pending.
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default=APPROVED, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = ProjectQuerySet.as_manager()

    class Meta:
        ordering = ['-featured', 'order', '-created_at']

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = _unique_slug(Project, self.title, self.pk, 'project')
        super().save(*args, **kwargs)

    @property
    def video_embed_url(self):
        """Embeddable iframe URL for YouTube/Loom links; '' for anything else."""
        u = urlparse(self.demo_video_url)
        host = (u.hostname or '').removeprefix('www.')
        if host == 'youtu.be' and u.path.strip('/'):
            return f"https://www.youtube-nocookie.com/embed/{u.path.strip('/')}"
        if host in ('youtube.com', 'm.youtube.com'):
            vid = parse_qs(u.query).get('v', [''])[0]
            if u.path.startswith('/embed/'):
                vid = u.path.split('/')[2] if len(u.path.split('/')) > 2 else ''
            if vid:
                return f"https://www.youtube-nocookie.com/embed/{vid}"
        if host == 'loom.com' and u.path.startswith('/share/'):
            return f"https://www.loom.com{u.path.replace('/share/', '/embed/', 1)}"
        return ''


class ProjectImage(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='projects/gallery/')
    caption = models.CharField(max_length=200, blank=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order', 'pk']

    def __str__(self):
        return self.caption or f"Image for {self.project}"


class TeamMember(models.Model):
    name = models.CharField(max_length=200)
    role = models.CharField(max_length=100, help_text='e.g. President, Treasurer')
    term = models.CharField(max_length=20, default=current_term_key, db_index=True,
                            help_text='Which executive board this member served on')
    major = models.CharField(max_length=200, blank=True, help_text='e.g. Computer Science, Senior')
    is_ambassador = models.BooleanField(default=False, help_text='Official Anthropic Campus Ambassador')
    builder = models.ForeignKey('Builder', null=True, blank=True, on_delete=models.SET_NULL,
                                related_name='team_members',
                                help_text='Link this member\'s card to their builder profile')
    linkedin = models.URLField(blank=True, default='')
    photo = models.ImageField(upload_to='team/', blank=True)
    # Only used for the original members whose photos live in static files.
    # A photo uploaded in the dashboard takes priority over this.
    legacy_static_image = models.CharField(max_length=300, blank=True, default='', editable=False)
    order = models.PositiveIntegerField(default=0, help_text='Lower numbers appear first')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['order', 'created_at']

    def __str__(self):
        return f"{self.name} ({self.role})"

    @property
    def term_label(self):
        return term_label(self.term)

    @property
    def initials(self):
        parts = self.name.replace('.', ' ').split()
        if not parts:
            return '?'
        if len(parts) == 1:
            return parts[0][0].upper()
        return (parts[0][0] + parts[-1][0]).upper()

    @property
    def image_url(self):
        if self.photo:
            return self.photo.url
        if self.legacy_static_image:
            return static(self.legacy_static_image)
        return ''
