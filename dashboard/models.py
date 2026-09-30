from django.db import models
from django.templatetags.static import static


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
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['date', 'start_time']

    def __str__(self):
        return f"{self.title} ({self.date})"

    def _format_time(self, t):
        """Format time as '2:00 PM' — works on both Windows and Unix."""
        return t.strftime('%I:%M %p').lstrip('0')

    def to_template_dict(self):
        """Format event data the way landing/index.html expects it."""
        return {
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


class Project(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    image = models.ImageField(upload_to='projects/', blank=True)
    tech = models.JSONField(default=list, help_text='List of tech tags, e.g. ["Next.js", "Supabase"]')
    link = models.URLField(blank=True, default='')
    coming_soon = models.BooleanField(default=False)
    order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['order', '-created_at']

    def __str__(self):
        return self.title


class TeamMember(models.Model):
    name = models.CharField(max_length=200)
    role = models.CharField(max_length=100, help_text='e.g. President, Treasurer')
    major = models.CharField(max_length=200, blank=True, help_text='e.g. Computer Science, Senior')
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
