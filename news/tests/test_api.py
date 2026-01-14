from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status

from news.models import CustomUser, Publisher, Article


class ArticleAPITestCase(APITestCase):

    def setUp(self):
        # Create users
        self.reader = CustomUser.objects.create_user(
            username='reader',
            email='reader@test.com',
            password='password123',
            role='reader'
        )

        self.journalist = CustomUser.objects.create_user(
            username='journalist',
            email='journalist@test.com',
            password='password123',
            role='journalist'
        )

        self.other_journalist = CustomUser.objects.create_user(
            username='other',
            email='other@test.com',
            password='password123',
            role='journalist'
        )

        # Create publisher
        self.publisher = Publisher.objects.create(name='Daily News')

        # Reader subscribes
        self.reader.subscribed_publishers.add(self.publisher)
        self.reader.subscribed_journalists.add(self.journalist)

        # Create approved article (should be visible)
        self.approved_article = Article.objects.create(
            title='Approved Article',
            content='Approved content',
            author=self.journalist,
            publisher=self.publisher,
            approved=True
        )

        # Create unapproved article (should NOT be visible)
        self.unapproved_article = Article.objects.create(
            title='Unapproved Article',
            content='Draft content',
            author=self.journalist,
            publisher=self.publisher,
            approved=False
        )

        # Create article by non-subscribed journalist
        self.other_article = Article.objects.create(
            title='Other Journalist Article',
            content='Other content',
            author=self.other_journalist,
            approved=True
        )

        # Authenticate reader
        self.client.login(
            username='reader',
            password='password123'
        )

    # -------------------------
    # TEST: Subscribed articles
    # -------------------------
    def test_subscribed_articles_api(self):
        url = reverse('api_subscribed_articles')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        titles = [article['title'] for article in response.data]

        self.assertIn('Approved Article', titles)
        self.assertNotIn('Unapproved Article', titles)
        self.assertNotIn('Other Journalist Article', titles)

    # -------------------------
    # TEST: Publisher articles
    # -------------------------
    def test_publisher_articles_api(self):
        url = reverse('api_publisher_articles', args=[self.publisher.id])
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        titles = [article['title'] for article in response.data]

        self.assertIn('Approved Article', titles)
        self.assertNotIn('Unapproved Article', titles)

    # -------------------------
    # TEST: Journalist articles
    # -------------------------
    def test_journalist_articles_api(self):
        url = reverse('api_journalist_articles', args=[self.journalist.id])
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        titles = [article['title'] for article in response.data]

        self.assertIn('Approved Article', titles)
        self.assertNotIn('Unapproved Article', titles)
