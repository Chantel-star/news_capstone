from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, permission_required, user_passes_test
from .models import Article, Publisher, CustomUser
from .forms import ArticleForm  

# =====================================
# Article Views
# =====================================

def article_list(request):
    """
    List all approved articles.
    """
    articles = Article.objects.filter(approved=True).order_by('-created_at')
    return render(request, 'news/article_list.html', {'articles': articles})


def article_detail(request, article_id):
    """
    Show a single article detail page.
    """
    article = get_object_or_404(Article, id=article_id)
    return render(request, 'news/article_detail.html', {'article': article})


# =====================================
# Editor Dashboard & Approval Views
# =====================================

@login_required
@user_passes_test(lambda u: u.role == 'editor')
def editor_dashboard(request):
    """
    Dashboard showing articles waiting for approval.
    """
    pending_articles = Article.objects.filter(approved=False)
    return render(request, 'news/editor_dashboard.html', {'pending_articles': pending_articles})


@login_required
@user_passes_test(lambda u: u.role == 'editor')
def approve_article(request, article_id):
    """
    Approve an article.
    """
    article = get_object_or_404(Article, id=article_id)
    article.approved = True
    article.save()  # Signals will handle notifications
    return redirect('editor_dashboard')


# =====================================
# Subscription Views 
# =====================================

@login_required
def subscribe_publisher(request, publisher_id):
    """
    Allows a reader to subscribe/unsubscribe to a Publisher.
    """
    publisher = get_object_or_404(Publisher, id=publisher_id)
    user = request.user

    if user.role != 'reader':
        return redirect('article_list')

    if publisher in user.subscribed_publishers.all():
        user.subscribed_publishers.remove(publisher)
    else:
        user.subscribed_publishers.add(publisher)

    return redirect('publisher_list')


@login_required
def subscribe_journalist(request, journalist_id):
    """
    Allows a reader to subscribe/unsubscribe to a Journalist.
    """
    journalist = get_object_or_404(CustomUser, id=journalist_id, role='journalist')
    user = request.user

    if user.role != 'reader':
        return redirect('article_list')

    if journalist in user.subscribed_journalists.all():
        user.subscribed_journalists.remove(journalist)
    else:
        user.subscribed_journalists.add(journalist)

    return redirect('journalist_list')
