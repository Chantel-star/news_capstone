from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings
import requests

from django.apps import apps

# Get your models dynamically
Article = apps.get_model('news', 'Article')
CustomUser = apps.get_model('news', 'CustomUser')
Publisher = apps.get_model('news', 'Publisher')


@receiver(post_save, sender=Article)
def article_approved_signal(sender, instance, created, **kwargs):
    """
    Triggered when an article is approved.
    Sends emails to subscribers and posts to X (optional).
    """
    # Only trigger when article is updated (not created) and approved
    if not created and instance.approved:

        recipients = set()

        # Subscribers to the publisher
        if instance.publisher:
            for reader in instance.publisher.subscribed_readers.all():
                recipients.add(reader.email)

        # Subscribers to the journalist
        if instance.author:
            for reader in instance.author.journalist_subscribers.all():
                recipients.add(reader.email)

        # Send email notifications
        subject = f"New Article Published: {instance.title}"
        message = f"{instance.content[:200]}...\nRead more on our site!"
        from_email = settings.DEFAULT_FROM_EMAIL

        for email in recipients:
            try:
                send_mail(subject, message, from_email, [email])
            except Exception as e:
                print(f"Failed to send email to {email}: {e}")

        # Post to X (Twitter) using requests
        try:
            X_BEARER_TOKEN = getattr(settings, 'X_BEARER_TOKEN', None)
            if X_BEARER_TOKEN:
                X_API_URL = 'https://api.twitter.com/2/tweets'
                headers = {
                    "Authorization": f"Bearer {X_BEARER_TOKEN}",
                    "Content-Type": "application/json"
                }
                payload = {"text": f"New Article Published: {instance.title}\nRead here!"}
                response = requests.post(X_API_URL, json=payload, headers=headers)
                if response.status_code != 201:
                    print(f"X API error: {response.status_code} - {response.text}")
        except Exception as e:
            print(f"Failed to post to X: {e}")
