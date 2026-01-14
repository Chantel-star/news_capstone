from django.contrib.auth.decorators import (
    login_required,
    permission_required,
)
from django.shortcuts import get_object_or_404, render, redirect

from .models import Article

# Ensure Article model is properly imported from models

@login_required
def article_list(request):
    """
    Display approved articles only.
    """
    articles = Article.objects.filter(approved=True)
    return render(request, 'news/article_list.html', {
        'articles': articles
    })

@login_required
def article_detail(request, article_id):
    """
    Display a single approved article.
    """
    article = get_object_or_404(
        Article,
        id=article_id,
        approved=True
    )
    return render(request, 'news/article_detail.html', {
        'article': article
    })

@permission_required('news.change_article')
def editor_dashboard(request):
    """
    Dashboard for editors to review articles.
    """
    articles = Article.objects.filter(approved=False)
    return render(request, 'news/editor_dashboard.html', {
        'articles': articles
    })

@permission_required('news.change_article')
def approve_article(request, article_id):
    """
    Approve an article for publishing.
    """
    article = get_object_or_404(Article, id=article_id)

    if request.method == 'POST':
        article.approved = True
        article.save()
        return redirect('editor_dashboard')

    return render(request, 'news/approve_article.html', {
        'article': article
    })
