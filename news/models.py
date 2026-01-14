from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    ROLE_CHOICES = (
        ('reader', 'Reader'),
        ('journalist', 'Journalist'),
        ('editor', 'Editor'),
    )

    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES
    )


class Publisher(models.Model):
    name = models.CharField(max_length=255)

    editors = models.ManyToManyField(
        CustomUser,
        related_name='editor_publishers',
        limit_choices_to={'role': 'editor'},
        blank=True
    )

    journalists = models.ManyToManyField(
        CustomUser,
        related_name='journalist_publishers',
        limit_choices_to={'role': 'journalist'},
        blank=True
    )


class Article(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()

    author = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        limit_choices_to={'role': 'journalist'},
        default=1 # Default to user with ID 1
    )

    publisher = models.ForeignKey(
        Publisher,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    approved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    
   