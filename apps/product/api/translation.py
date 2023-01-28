from modeltranslation.translator import translator, TranslationOptions
from apps.product.models import Product


class ProductTranslationOptions(TranslationOptions):
    fields = ('name', 'slug', 'consists')


translator.register(Product, ProductTranslationOptions)
