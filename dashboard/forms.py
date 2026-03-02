from django import forms
from .models import Event, GalleryImage, Project


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
        fields = ['title', 'description', 'location', 'date', 'start_time', 'end_time']
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Event title'}),
            'description': forms.Textarea(attrs={'placeholder': 'Event description', 'rows': 3}),
            'location': forms.TextInput(attrs={'placeholder': 'e.g. Lafferre Hall, Room 100'}),
            'date': forms.DateInput(attrs={'type': 'date'}),
            'start_time': forms.TimeInput(attrs={'type': 'time'}),
            'end_time': forms.TimeInput(attrs={'type': 'time'}),
        }


class ProjectForm(forms.ModelForm):
    tech_input = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'placeholder': 'e.g. Next.js, Supabase, Tailwind CSS'}),
        help_text='Comma-separated list of technologies.',
    )

    class Meta:
        model = Project
        fields = ['title', 'description', 'image', 'link', 'coming_soon', 'order']
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Project name'}),
            'description': forms.Textarea(attrs={'placeholder': 'What does this project do?', 'rows': 3}),
            'link': forms.URLInput(attrs={'placeholder': 'https://...'}),
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
        return instance