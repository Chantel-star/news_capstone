from django.contrib.auth.models import Group, Permission
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.apps import apps
from django.conf import settings
from django.core.mail import send_mail
import requests

from .models import CustomUser

# -----------------------------
# Setup Groups & Permissions
# -----------------------------
def setup_groups():
    """
    Create groups and assign permissions.
    Runs safely even if groups already exist.
    """
    Article = apps.get_model('news', 'Article')  # Safe dynamic import

    reader_group, _ = Group.objects.get_or_create(name='Reader')
    journalist_group, _ = Group.objects.get_or_create(name='Journalist')
    editor_group, _ = Group.objects.get_or_create(name='Editor')

    # Reader permissions
    reader_perms = Permission.objects.filter(
        content_type__app_label='news',
        codename__in=['view_article']
    )
    reader_group.permissions.set(reader_perms)

    # Journalist permissions
    journalist_perms = Permission.objects.filter(
        content_type__app_label='news',
        codename__in=[
            'add_article',
            'view_article',
            'change_article',
            'delete_article',
        ]
    )
    journalist_group.permissions.set(journalist_perms)

    # Editor permissions
    editor_perms = Permission.objects.filter(
        content_type__app_label='news',
        codename__in=[
            'view_article',
            'change_article',
            'delete_article',
        ]
    )
    editor_group.permissions.set(editor_perms)

# -----------------------------
# Auto-assign user to group
# -----------------------------
@receiver(post_save, sender=CustomUser)
def assign_user_to_group(sender, instance, created, **kwargs):
    if not created:
        return

    setup_groups()

    role_to_group = {
        'reader': 'Reader',
        'journalist': 'Journalist',
        'editor': 'Editor',
    }

    group_name = role_to_group.get(instance.role)
    if group_name:
        group = Group.objects.get(name=group_name)
        instance.groups.add(group)

# -----------------------------
# Article approval signal
# -----------------------------
Article = apps.get_model('news', 'Article')  # dynamic import again

@receiver(post_save, sender=Article)
def article_approved_signal(sender, instance, created, **kwargs):
    """
    Triggered when an article is approved.
    Sends emails to subscribed readers and posts to X.
    """
    if not created and instance.approved:
        recipients = set()

        # Subscribers to publisher
        if instance.publisher:
            for reader in instance.publisher.subscribed_readers.all():
                recipients.add(reader.email)

        # Subscribers to journalist
        for reader in instance.author.journalist_subscribers.all():
            recipients.add(reader.email)

        # Send email
        subject = f"New Article Published: {instance.title}"
        message = f"{instance.content[:200]}...\nRead more on our site!"
        from_email = settings.DEFAULT_FROM_EMAIL

        for email in recipients:
            try:
                send_mail(subject, message, from_email, [email])
            except Exception as e:
                print(f"Failed to send email to {email}: {e}")

        # Post to X (Twitter)
        try:
            X_BEARER_TOKEN = 'YOUR_X_BEARER_TOKEN'
            X_API_URL = 'https://api.twitter.com/2/tweets'

            headers = {
                "Authorization": f"Bearer {X_BEARER_TOKEN}",
                "Content-Type": "application/json"
            }

            payload = {
                "text": f"New Article Published: {instance.title}\nRead here!"
            }

            response = requests.post(X_API_URL, json=payload, headers=headers)
            if response.status_code != 201:
                print(f"X API error: {response.status_code} - {response.text}")
        except Exception as e:
            print(f"Failed to post to X: {e}")
