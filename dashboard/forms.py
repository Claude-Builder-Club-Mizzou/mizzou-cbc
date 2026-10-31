from django import forms
from .models import Builder, Event, GalleryImage, Project, ProjectImage, TeamMember
from .terms import all_terms, term_label


class GalleryImageForm(forms.ModelForm):
    class Meta:
        model = GalleryImage
        fields = ['caption', 'image', 'order']
        widgets = {
            'caption': forms.TextInput(attrs={'placeholder': 'Photo caption'}),
            'order': forms.NumberInput(attrs={'min': 0}),
        }


class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['title', 'description', 'location', 'date', 'start_time', 'end_time', 'rsvp_url']
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Event title'}),
            'description': forms.Textarea(attrs={'placeholder': 'Event description', 'rows': 3}),
            'location': forms.TextInput(attrs={'placeholder': 'e.g. Lafferre Hall, Room 100'}),
            'date': forms.DateInput(attrs={'type': 'date'}),
            'start_time': forms.TimeInput(attrs={'type': 'time'}),
            'end_time': forms.TimeInput(attrs={'type': 'time'}),
            'rsvp_url': forms.URLInput(attrs={'placeholder': 'https://... (campus RSVP link)'}),
        }


class ProjectForm(forms.ModelForm):
    tech_input = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'placeholder': 'e.g. Next.js, Supabase, Tailwind CSS'}),
        help_text='Comma-separated list of technologies.',
    )

    class Meta:
        model = Project
        fields = [
            'title', 'description', 'image', 'builders',
            'story', 'claude_usage', 'challenges',
            'link', 'github_url', 'demo_video_url',
            'built_at', 'coming_soon', 'featured', 'order',
        ]
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Project name'}),
            'description': forms.Textarea(attrs={'placeholder': 'One or two sentences for the project card', 'rows': 3}),
            'builders': forms.CheckboxSelectMultiple,
            'story': forms.Textarea(attrs={'placeholder': 'What it is, why you built it, how it works. Blank lines start a new paragraph.', 'rows': 8}),
            'claude_usage': forms.Textarea(attrs={'placeholder': 'Which Claude models or tools did you use, and for what?', 'rows': 5}),
            'challenges': forms.Textarea(attrs={'placeholder': 'What was hard? What would you do differently?', 'rows': 5}),
            'link': forms.URLInput(attrs={'placeholder': 'https://... (live site or app)'}),
            'github_url': forms.URLInput(attrs={'placeholder': 'https://github.com/...'}),
            'demo_video_url': forms.URLInput(attrs={'placeholder': 'https://youtu.be/... or a Loom link'}),
            'built_at': forms.TextInput(attrs={'placeholder': 'e.g. Spring 2026 Hackathon'}),
            'order': forms.NumberInput(attrs={'min': 0}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            self.fields['tech_input'].initial = ', '.join(self.instance.tech or [])

    def clean_tech_input(self):
        raw = self.cleaned_data.get('tech_input', '')
        return [tag.strip() for tag in raw.split(',') if tag.strip()]

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.tech = self.cleaned_data['tech_input']
        if commit:
            instance.save()
            self.save_m2m()
        return instance


ProjectImageFormSet = forms.inlineformset_factory(
    Project, ProjectImage,
    fields=['image', 'caption', 'order'],
    extra=3,
    can_delete=True,
    widgets={
        'caption': forms.TextInput(attrs={'placeholder': 'Caption (optional)'}),
        'order': forms.NumberInput(attrs={'min': 0}),
    },
)


class BuilderForm(forms.ModelForm):
    class Meta:
        model = Builder
        fields = ['name', 'major', 'year', 'bio', 'photo', 'linkedin', 'github', 'website']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Full name'}),
            'major': forms.TextInput(attrs={'placeholder': 'e.g. Computer Science'}),
            'year': forms.TextInput(attrs={'placeholder': 'e.g. Junior'}),
            'bio': forms.Textarea(attrs={'placeholder': 'A sentence or two about this builder', 'rows': 3}),
            'linkedin': forms.URLInput(attrs={'placeholder': 'https://www.linkedin.com/in/...'}),
            'github': forms.URLInput(attrs={'placeholder': 'https://github.com/...'}),
            'website': forms.URLInput(attrs={'placeholder': 'https://...'}),
        }


class TeamMemberForm(forms.ModelForm):
    class Meta:
        model = TeamMember
        fields = ['name', 'role', 'term', 'major', 'is_ambassador', 'builder', 'linkedin', 'photo', 'order']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Full name'}),
            'role': forms.TextInput(attrs={'placeholder': 'e.g. President'}),
            'major': forms.TextInput(attrs={'placeholder': 'e.g. Computer Science, Senior'}),
            'linkedin': forms.URLInput(attrs={'placeholder': 'https://www.linkedin.com/in/...'}),
            'order': forms.NumberInput(attrs={'min': 0}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        choices = all_terms()
        # Keep an out-of-range term selectable so editing never silently changes it.
        if self.instance.pk and self.instance.term not in dict(choices):
            choices.append((self.instance.term, term_label(self.instance.term)))
        self.fields['term'] = forms.ChoiceField(choices=choices, initial=self.fields['term'].initial)
