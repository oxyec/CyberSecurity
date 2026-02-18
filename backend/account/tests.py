from django.test import TestCase, Client, override_settings
from django.contrib.auth import get_user_model
from django.core.cache import cache
from unittest.mock import patch
from account.models import LoginAttempt

@override_settings(SECURE_SSL_REDIRECT=False)
class LoginRateLimitTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = get_user_model().objects.create_user(username='testuser', password='password123')
        cache.clear()
        LoginAttempt.objects.all().delete()

    @patch('django.contrib.auth.forms.authenticate')
    def test_rate_limit_enforcement(self, mock_authenticate):
        # Setup mock to fail authentication but return None (standard behavior)
        mock_authenticate.return_value = None

        url = '/accounts/login/'

        # Make 6 failed login attempts
        for i in range(6):
            response = self.client.post(url, {'username': 'testuser', 'password': 'wrongpassword'})

            # For the first 4 attempts (0, 1, 2, 3), we expect standard failure behavior (form invalid)
            # For the 5th attempt (index 4), the logic says:
            # failures append -> len is 5 -> redirect.
            # But form_invalid runs AFTER authenticate.

            if i < 4:
                # Should be on login page with error
                if response.status_code != 200:
                    print(f"Attempt {i+1} status: {response.status_code}")
                self.assertEqual(response.status_code, 200, f"Attempt {i+1} failed")
                # Messages should contain "Kullanıcı adı veya şifre yanlış."
            else:
                # 5th and 6th attempt should redirect
                if response.status_code != 302:
                    print(f"Attempt {i+1} status: {response.status_code}")
                self.assertEqual(response.status_code, 302, f"Attempt {i+1} failed (expected redirect)")

        # Verify authenticate was called 5 times (once for each valid attempt)
        # Because the rate limit check now happens in dispatch, blocking the 6th attempt early
        print(f"Call count: {mock_authenticate.call_count}")
        self.assertEqual(mock_authenticate.call_count, 5)
