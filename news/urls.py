from django.urls import path
from . import views

urlpatterns = [
    path('', views.article_list, name='article_list'),
    path('article/<int:article_id>/', views.article_detail,
         name='article_detail'),
    path('editor/', views.editor_dashboard,
         name='editor_dashboard'),
    path('approve/<int:article_id>/', views.approve_article,
         name='approve_article'),
]


