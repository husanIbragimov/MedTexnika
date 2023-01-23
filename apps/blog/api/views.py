from rest_framework import generics
from apps.blog.models import Article
from apps.blog.api.serializers import ArticleSerializer


class ArticleListAPIView(generics.ListAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer


class ArticleRetrieveDestroyAPIView(generics.RetrieveDestroyAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    lookup_field = 'pk'
