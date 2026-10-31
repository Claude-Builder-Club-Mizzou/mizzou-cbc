import tempfile
from datetime import time, timedelta

from django.test import TestCase, override_settings
from django.urls import reverse
from django.utils import timezone

from dashboard.models import Event, Project


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


@override_settings(SITE_URL='https://claudebuilderclub.com', MEDIA_ROOT=tempfile.mkdtemp())
class ProjectSubmissionTests(TestCase):
    def _png(self, name='x.png'):
        import io
        from PIL import Image
        from django.core.files.uploadedfile import SimpleUploadedFile
        buf = io.BytesIO()
        Image.new('RGB', (4, 4), 'red').save(buf, 'PNG')
        return SimpleUploadedFile(name, buf.getvalue(), content_type='image/png')

    def _payload(self, **over):
        data = {
            'builder-name': 'Ada Lovelace', 'builder-email': 'ada@example.com',
            'builder-bio': 'I build things.',
            'project-title': 'Cool App', 'project-description': 'It is cool.',
            'project-story': 'Long story.', 'project-claude_usage': 'Claude Code.',
            'project-tech_input': 'Django, Claude',
            'project-github_url': 'https://github.com/ada/cool',
            'project-image': self._png(),
            'images-TOTAL_FORMS': 3, 'images-INITIAL_FORMS': 0,
            'images-MIN_NUM_FORMS': 0, 'images-MAX_NUM_FORMS': 3,
        }
        data.update(over)
        return data

    def test_form_renders(self):
        self.assertEqual(self.client.get(reverse('submit_project')).status_code, 200)
        self.assertEqual(self.client.get(reverse('submit_thanks')).status_code, 200)

    def test_submission_is_pending_hidden_and_emails_exec(self):
        from django.core import mail
        from dashboard.models import Builder, Project
        res = self.client.post(reverse('submit_project'), self._payload())
        self.assertRedirects(res, reverse('submit_thanks'))
        p = Project.objects.get(title='Cool App')
        b = Builder.objects.get(name='Ada Lovelace')
        self.assertEqual(p.status, Project.PENDING)
        self.assertFalse(b.is_approved)
        self.assertEqual(list(p.builders.all()), [b])
        self.assertEqual(p.tech, ['Django', 'Claude'])
        # Not visible anywhere public.
        self.assertNotContains(self.client.get(reverse('projects')), 'Cool App')
        self.assertEqual(self.client.get(reverse('project_detail', args=[p.slug])).status_code, 404)
        self.assertEqual(self.client.get(reverse('builder_detail', args=[b.slug])).status_code, 404)
        # Exec inbox notified, reply goes to the builder.
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].to, ['cbcmizzou@gmail.com'])
        self.assertIn('Cool App', mail.outbox[0].subject)
        self.assertEqual(mail.outbox[0].reply_to, ['ada@example.com'])
        html = mail.outbox[0].alternatives[0][0]
        self.assertIn('Cool App', html)
        self.assertIn('https://claudebuilderclub.com/cb-exec/dashboard/submissions/', html)
        self.assertIn('https://claudebuilderclub.com/media/projects/', html)
        self.assertIn('https://claudebuilderclub.com/cb-exec/dashboard/submissions/', mail.outbox[0].body)

    def test_email_html_escapes_user_input(self):
        from django.core import mail
        self.client.post(reverse('submit_project'), self._payload(**{'project-title': '<script>x</script>'}))
        html = mail.outbox[0].alternatives[0][0]
        self.assertNotIn('<script>x</script>', html)
        self.assertIn('&lt;script&gt;', html)

    def test_validation_requires_a_link_and_email(self):
        from dashboard.models import Project
        res = self.client.post(reverse('submit_project'),
                               self._payload(**{'project-github_url': '', 'builder-email': 'nope'}))
        self.assertEqual(res.status_code, 200)
        self.assertContains(res, 'Add at least one link')
        self.assertEqual(Project.objects.count(), 0)

    def test_honeypot_saves_nothing(self):
        from django.core import mail
        from dashboard.models import Project
        res = self.client.post(reverse('submit_project'), self._payload(company='spam inc'))
        self.assertRedirects(res, reverse('submit_thanks'))
        self.assertEqual(Project.objects.count(), 0)
        self.assertEqual(len(mail.outbox), 0)

    def test_email_failure_does_not_lose_submission(self):
        from unittest import mock
        from dashboard.models import Project
        with mock.patch('django.core.mail.EmailMessage.send', side_effect=OSError('smtp down')):
            with self.assertLogs('dashboard.notifications', level='ERROR'):
                res = self.client.post(reverse('submit_project'), self._payload())
        self.assertRedirects(res, reverse('submit_thanks'))
        self.assertEqual(Project.objects.pending().count(), 1)


@override_settings(MEDIA_ROOT=tempfile.mkdtemp())
class SubmissionReviewTests(TestCase):
    def setUp(self):
        from django.contrib.auth import get_user_model
        from dashboard.models import Builder, Project
        self.builder = Builder.objects.create(name='Ada', email='a@x.com', is_approved=False)
        self.project = Project.objects.create(title='Pending One', description='d', status=Project.PENDING)
        self.project.builders.add(self.builder)
        self.client.force_login(get_user_model().objects.create_user('exec', password='x'))

    def test_queue_requires_login_and_lists_pending(self):
        res = self.client.get(reverse('dashboard:submissions'))
        self.assertContains(res, 'Pending One')
        self.client.logout()
        self.assertEqual(self.client.get(reverse('dashboard:submissions')).status_code, 302)
        self.assertEqual(self.client.post(reverse('dashboard:submission_approve', args=[self.project.pk])).status_code, 302)
        self.project.refresh_from_db()
        self.assertEqual(self.project.status, 'pending')

    def test_approve_publishes_project_and_builder(self):
        self.client.post(reverse('dashboard:submission_approve', args=[self.project.pk]))
        self.project.refresh_from_db()
        self.builder.refresh_from_db()
        self.assertEqual(self.project.status, 'approved')
        self.assertTrue(self.builder.is_approved)
        self.client.logout()
        self.assertContains(self.client.get(reverse('projects')), 'Pending One')
        self.assertEqual(self.client.get(reverse('builder_detail', args=[self.builder.slug])).status_code, 200)

    def test_reject_keeps_hidden_and_get_does_nothing(self):
        self.client.get(reverse('dashboard:submission_reject', args=[self.project.pk]))
        self.project.refresh_from_db()
        self.assertEqual(self.project.status, 'pending')
        self.client.post(reverse('dashboard:submission_reject', args=[self.project.pk]))
        self.project.refresh_from_db()
        self.assertEqual(self.project.status, 'rejected')
        self.client.logout()
        self.assertNotContains(self.client.get(reverse('projects')), 'Pending One')

    def test_delete_only_rejected_and_cleans_up_orphan_builder(self):
        from dashboard.models import Builder, Project
        url = reverse('dashboard:submission_delete', args=[self.project.pk])
        # A pending submission can't be deleted this way.
        self.client.post(url)
        self.assertTrue(Project.objects.filter(pk=self.project.pk).exists())
        self.client.post(reverse('dashboard:submission_reject', args=[self.project.pk]))
        # GET does nothing.
        self.client.get(url)
        self.assertTrue(Project.objects.filter(pk=self.project.pk).exists())
        self.client.post(url)
        self.assertFalse(Project.objects.filter(pk=self.project.pk).exists())
        self.assertFalse(Builder.objects.filter(pk=self.builder.pk).exists())

    def test_delete_keeps_builder_with_other_projects(self):
        from dashboard.models import Builder, Project
        other = Project.objects.create(title='Other', description='d')
        other.builders.add(self.builder)
        self.client.post(reverse('dashboard:submission_reject', args=[self.project.pk]))
        self.client.post(reverse('dashboard:submission_delete', args=[self.project.pk]))
        self.assertTrue(Builder.objects.filter(pk=self.builder.pk).exists())

    def test_delete_requires_login(self):
        from dashboard.models import Project
        self.client.post(reverse('dashboard:submission_reject', args=[self.project.pk]))
        self.client.logout()
        self.client.post(reverse('dashboard:submission_delete', args=[self.project.pk]))
        self.assertTrue(Project.objects.filter(pk=self.project.pk).exists())


@override_settings(SITE_URL='https://claudebuilderclub.com')
class CrawlerFilesTests(TestCase):
    def setUp(self):
        Project.objects.create(title='Live One', description='Does a thing.\nWith Claude.')
        Project.objects.create(title='Hidden One', description='Pending.', status=Project.PENDING)

    def test_llms_txt_lists_approved_projects_only(self):
        r = self.client.get('/llms.txt')
        self.assertEqual(r.status_code, 200)
        self.assertTrue(r['Content-Type'].startswith('text/plain'))
        text = r.content.decode()
        self.assertTrue(text.startswith('# Claude Builder Club @ Mizzou'))
        self.assertIn('https://claudebuilderclub.com/projects/live-one/', text)
        self.assertIn('Does a thing. With Claude.', text)
        self.assertNotIn('Hidden One', text)

    def test_robots_txt_points_at_sitemap_and_blocks_admin(self):
        text = self.client.get('/robots.txt').content.decode()
        self.assertIn('Disallow: /cb-exec/', text)
        self.assertIn('Sitemap: https://claudebuilderclub.com/sitemap.xml', text)

    def test_sitemap_has_pages_and_approved_projects(self):
        r = self.client.get('/sitemap.xml')
        self.assertEqual(r['Content-Type'], 'application/xml')
        text = r.content.decode()
        self.assertIn('<loc>https://claudebuilderclub.com/benefits/</loc>', text)
        self.assertIn('/projects/live-one/', text)
        self.assertNotIn('hidden-one', text)
