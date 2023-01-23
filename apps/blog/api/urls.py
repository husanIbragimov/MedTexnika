from django.urls import path
from apps.blog.api.views import ArticleListAPIView, ArticleRetrieveAPIView

urlpatterns = [
    path('article-list', ArticleListAPIView.as_view()),
    path('article-rd/<int:pk>/', ArticleRetrieveAPIView.as_view()),
]
