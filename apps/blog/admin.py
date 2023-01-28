from django.contrib import admin
from .models import Article
from modeltranslation.admin import TranslationAdmin


class ArticleAdmin(TranslationAdmin):
    search_fields = ('id', 'title', 'content', 'created_at')
    list_display = ('id', 'title',)
    prepopulated_fields = {"slug": ("title",)}


admin.site.register(Article, ArticleAdmin)
