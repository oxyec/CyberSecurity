from django.test import TestCase, Client, override_settings
from django.urls import reverse
from blog.models import Post
from django.contrib.auth import get_user_model

User = get_user_model()

@override_settings(SECURE_SSL_REDIRECT=False)
class BlogPerformanceTest(TestCase):
    def setUp(self):
        self.client = Client()
        try:
            self.url = reverse('blog_list')
        except:
            self.url = '/blog_list/' # Fallback
        self.user1 = User.objects.create_user(username='user1', password='password')
        self.user2 = User.objects.create_user(username='user2', password='password')

    def test_blog_list_queries(self):
        """
        Verify that blog_list view uses select_related to avoid N+1 query problem.
        Expect constant number of queries (1) regardless of number of posts.
        """
        # Create 10 posts
        for i in range(5):
            Post.objects.create(title=f'Post {i}', content='Content', author=self.user1)
        for i in range(5):
            Post.objects.create(title=f'Post {i}', content='Content', author=self.user2)

        # Expect 1 query because select_related joins the author table.
        # Without optimization, this would be 1 + 10 = 11 queries.
        with self.assertNumQueries(1):
            response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
