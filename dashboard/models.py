from django.db import models


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