from datetime import time, timedelta

from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from dashboard.models import Event


class HomeEventsTests(TestCase):
    def test_home_exposes_rsvp_url(self):
        Event.objects.create(
            title='Workshop', description='d', location='Lafferre',
            date=timezone.localdate() + timedelta(days=3),
            start_time=time(18), end_time=time(19),
            rsvp_url='https://campus.example.edu/rsvp/1',
        )
        res = self.client.get(reverse('home'))
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.context['events'][0]['rsvp_url'], 'https://campus.example.edu/rsvp/1')


class ProjectDetailTests(TestCase):
    def setUp(self):
        from dashboard.models import Builder, Project, ProjectImage
        self.builder = Builder.objects.create(name='Ada Lovelace', major='Math', year='Senior')
        self.project = Project.objects.create(
            title='Mech::Forge', description='d', tech=['Django', 'Claude'],
            story='Line one.\n\nLine two <script>x</script>',
            demo_video_url='https://youtu.be/abc123', built_at='Spring Hackathon',
        )
        self.project.builders.add(self.builder)

    def test_slug_generated_and_unique(self):
        from dashboard.models import Project
        dup = Project.objects.create(title='Mech::Forge', description='d')
        self.assertEqual(self.project.slug, 'mechforge')
        self.assertEqual(dup.slug, 'mechforge-2')

    def test_list_links_to_detail_and_shows_built_at(self):
        res = self.client.get(reverse('projects'))
        self.assertContains(res, reverse('project_detail', args=['mechforge']))
        self.assertNotContains(res, 'tag-filter')
        self.assertContains(res, 'Spring Hackathon')

    def test_detail_renders_builders_video_and_escapes_story(self):
        res = self.client.get(reverse('project_detail', args=['mechforge']))
        self.assertEqual(res.status_code, 200)
        self.assertContains(res, 'Ada Lovelace')
        self.assertContains(res, 'youtube-nocookie.com/embed/abc123')
        self.assertNotContains(res, '<script>x</script>')

    def test_detail_404_and_builder_page(self):
        self.assertEqual(self.client.get(reverse('project_detail', args=['nope'])).status_code, 404)
        res = self.client.get(reverse('builder_detail', args=[self.builder.slug]))
        self.assertContains(res, 'Mech::Forge')

    def test_video_embed_url(self):
        from dashboard.models import Project
        cases = {
            'https://www.youtube.com/watch?v=XYZ': 'https://www.youtube-nocookie.com/embed/XYZ',
            'https://www.loom.com/share/abc': 'https://www.loom.com/embed/abc',
            'https://example.com/v.mp4': '',
            '': '',
        }
        for url, expected in cases.items():
            self.assertEqual(Project(demo_video_url=url).video_embed_url, expected, url)


class DashboardProjectTests(TestCase):
    def setUp(self):
        from django.contrib.auth import get_user_model
        self.client.force_login(get_user_model().objects.create_user('exec', password='x'))

    def test_pages_render(self):
        from dashboard.models import Project
        p = Project.objects.create(title='T', description='d')
        for name, args in [('dashboard:projects', []), ('dashboard:project_create', []),
                           ('dashboard:project_edit', [p.pk]), ('dashboard:builders', []),
                           ('dashboard:builder_create', [])]:
            self.assertEqual(self.client.get(reverse(name, args=args)).status_code, 200, name)

    def test_create_project_with_builder(self):
        from dashboard.models import Builder, Project
        b = Builder.objects.create(name='Grace Hopper')
        res = self.client.post(reverse('dashboard:project_create'), {
            'title': 'New', 'description': 'd', 'tech_input': 'A, B', 'order': 0,
            'builders': [b.pk], 'featured': 'on',
            'images-TOTAL_FORMS': 3, 'images-INITIAL_FORMS': 0,
            'images-MIN_NUM_FORMS': 0, 'images-MAX_NUM_FORMS': 1000,
            # Blank extra rows still post their default order, like a browser would.
            'images-0-order': 0, 'images-1-order': 0, 'images-2-order': 0,
        })
        self.assertEqual(res.status_code, 302)
        p = Project.objects.get(title='New')
        self.assertEqual(list(p.builders.all()), [b])
        self.assertTrue(p.featured)
