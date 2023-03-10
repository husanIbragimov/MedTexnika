from django.contrib import admin
from .models import Article
from modeltranslation.admin import TranslationAdmin


class ArticleAdmin(TranslationAdmin):
    search_fields = ('id', 'title', 'content')
    list_display = ('id', 'title', 'created_at')
    prepopulated_fields = {"slug": ("title",)}


admin.site.register(Article, ArticleAdmin)
