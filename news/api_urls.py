from django.urls import path
from . import api_views

urlpatterns = [
    path('articles/publisher/<int:pk>/', api_views.PublisherArticlesAPIView.as_view(),
         name='api_publisher_articles'),
    path('articles/journalist/<int:pk>/', api_views.JournalistArticlesAPIView.as_view(),
         name='api_journalist_articles'),
    path('articles/subscriptions/', api_views.SubscribedArticlesAPIView.as_view(),
         name='api_subscribed_articles'),
]
