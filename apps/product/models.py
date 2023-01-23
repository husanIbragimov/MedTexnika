from django.db import models
from django.urls import reverse

from apps.account.models import Account
from config import settings


class Timestamp(models.Model):
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True


class Category(models.Model):
    class Meta:
        verbose_name = "Mahsulot Kategoriyasi"
        verbose_name_plural = "Mahsulot Kategoriyalari"

    parent_category = models.ForeignKey('self', on_delete=models.CASCADE, verbose_name='Parent Category',
                                        limit_choices_to={'is_active': True, 'parent_category__isnull': True},
                                        related_name='children', null=True, blank=True, )
    title = models.CharField(max_length=223)
    is_active = models.BooleanField(default=True)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Brand(Timestamp):
    name = models.CharField(max_length=30)
    image = models.ImageField(upload_to='product/brands/')

    def __str__(self):
        return self.name


class CategoryStatus(Timestamp):
    name = models.CharField(max_length=100)

    @property
    def normalize_title(self):
        return self.name.replace(' ', '').lower()

    def __str__(self):
        return self.name


class NewValue(models.Model):
    new_price = models.CharField(max_length=20)

    def __str__(self):
        return self.new_price


class Product(Timestamp):
    STATUS = (
        (0, 'NEW'),
        (1, 'SALE'),
        (2, 'POPULAR'),
        (3, 'PREMIUM'),
    )
    status = models.IntegerField(choices=STATUS, default=0, verbose_name="Holati")
    name = models.CharField(max_length=223, null=True, verbose_name="Maxsulot nomi")
    slug = models.SlugField(unique=True, null=True, blank=True)
    category = models.ManyToManyField(Category, blank=True)
    brand = models.ForeignKey(Brand, on_delete=models.SET_NULL, null=True, blank=True)
    price = models.DecimalField(max_digits=15, decimal_places=2)
    discount = models.DecimalField(max_digits=3, decimal_places=2, null=True, blank=True)
    made_in = models.CharField(max_length=50)  # ishlab chiqarilgan joy
    consists = models.TextField()
    capacity = models.CharField(max_length=20)  # sig'imi
    guarantee = models.CharField(max_length=30)  # muddat
    is_active = models.BooleanField(default=True)

    def get_discounted_price(self):
        return self.price - (self.price * (self.discount / 100))

    def get_absolute_url(self):
        return reverse("product_detail", kwargs={"slug": self.slug})

    def __str__(self):
        return f'{self.name} | {self.id}'


class ProductImage(Timestamp):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, related_name='product_images')
    image = models.ImageField(upload_to='product/product_image/')
    is_active = models.BooleanField(default=True)

    @property
    def get_image_url(self):
        if settings.DEBUG:
            return f"{settings.LOCAL_BASE_URL}{self.image.url}"
        else:
            return f"{settings.PROD_BASE_URL}{self.image.url}"

    def __str__(self):
        return f'image of {self.product.id}'


class Banner(Timestamp):
    image = models.ImageField(upload_to='product/banner/')

    def __str__(self):
        return self.image.url
