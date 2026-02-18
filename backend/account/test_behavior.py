from django.test import TestCase, Client, override_settings
from django.contrib.auth import get_user_model
from django.core.cache import cache
from django.utils import timezone
from account.models import LoginAttempt
from datetime import timedelta

@override_settings(SECURE_SSL_REDIRECT=False)
class BehaviorAnalysisLeakTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = get_user_model().objects.create_user(username='victim', password='password123')
        self.attacker = get_user_model().objects.create_user(username='attacker', password='password123')
        LoginAttempt.objects.all().delete()

    def test_global_ip_leak_fixed(self):
        # Create a login attempt for another user (attacker) from a distinct IP
        LoginAttempt.objects.create(
            username='attacker',
            ip_address='10.0.0.99',  # Unique IP
            successful=True,
            timestamp=timezone.now()
        )

        # Create a login attempt for the victim from a different IP
        LoginAttempt.objects.create(
            username='victim',
            ip_address='192.168.1.1',
            successful=True,
            timestamp=timezone.now()
        )

        # Login as victim
        self.client.force_login(self.user)

        response = self.client.get('/users/behavior/')
        self.assertEqual(response.status_code, 200)

        # Attacker's IP should NOT be visible
        self.assertNotContains(response, '10.0.0.99')

        # Victim's own IP SHOULD be visible
        self.assertContains(response, '192.168.1.1')
