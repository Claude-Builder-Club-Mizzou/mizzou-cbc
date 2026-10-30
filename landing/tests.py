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
