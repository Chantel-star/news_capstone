from rest_framework import generics, permissions
from .models import Article, Publisher, CustomUser
from .serializers import ArticleSerializer

class PublisherArticlesAPIView(generics.ListAPIView):
    serializer_class = ArticleSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        publisher_id = self.kwargs['pk']
        return Article.objects.filter(
            publisher__id=publisher_id,
            approved=True
        )


class JournalistArticlesAPIView(generics.ListAPIView):
    serializer_class = ArticleSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        journalist_id = self.kwargs['pk']
        return Article.objects.filter(
            author__id=journalist_id,
            approved=True
        )


class SubscribedArticlesAPIView(generics.ListAPIView):
    serializer_class = ArticleSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        # Only approved articles
        articles = Article.objects.filter(approved=True)

        # Filter by subscriptions
        if hasattr(user, 'subscribed_publishers'):
            articles = articles.filter(
                publisher__in=user.subscribed_publishers.all()
            )

        if hasattr(user, 'subscribed_journalists'):
            articles = articles | articles.filter(
                author__in=user.subscribed_journalists.all()
            )

        return articles.distinct()
