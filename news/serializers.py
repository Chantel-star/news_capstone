from rest_framework import serializers
from .models import Article, Publisher, CustomUser

class PublisherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Publisher
        fields = ['id', 'name']

class JournalistSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'email', 'role']

class ArticleSerializer(serializers.ModelSerializer):
    author = JournalistSerializer(read_only=True)
    publisher = PublisherSerializer(read_only=True)

    class Meta:
        model = Article
        fields = [
            'id', 'title', 'content', 'author', 'publisher',
            'approved', 'created_at'
        ]
