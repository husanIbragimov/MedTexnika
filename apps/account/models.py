from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from rest_framework.reverse import reverse
from rest_framework_simplejwt.tokens import RefreshToken
from django.utils.translation import gettext_lazy as _


class AccountManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if email is None:
            raise TypeError('Email did not come')
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        if not password:
            raise TypeError('Password did not come')
        user = self.create_user(email, password, **extra_fields)
        user.is_superuser = True
        user.is_active = True
        user.is_admin = True
        user.is_staff = True
        user.save(using=self._db)
        return user


GENDER = (
    (0, 'None'),
    (1, 'Male'),
    (2, 'female'),
)


class Account(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True, db_index=True)
    username = models.CharField(max_length=100, unique=True, db_index=True)
    slug = models.SlugField(unique=True, null=True, blank=True)
    first_name = models.CharField(max_length=100, null=True)
    last_name = models.CharField(max_length=100, null=True)
    gender = models.IntegerField(choices=GENDER, default=0)
    image = models.ImageField(null=True, blank=True, upload_to='profile/')
    bio = models.TextField(null=True, blank=True)
    is_superuser = models.BooleanField(default=False, verbose_name='Super user')
    is_admin = models.BooleanField(default=False, verbose_name='Admin user')
    is_staff = models.BooleanField(default=False, verbose_name='Staff user')
    is_active = models.BooleanField(default=True, verbose_name='Active user')
    date_login = models.DateTimeField(auto_now=True, verbose_name='Last login')
    date_created = models.DateTimeField(auto_now_add=True, verbose_name='Created date')

    objects = AccountManager()

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        if self.first_name:
            return f'{self.first_name}'
        return f'{self.email}'

    def get_absolute_url(self):
        return reverse("account_detail", kwargs={"slug": self.slug})

    @property
    def token(self):
        refresh = RefreshToken.for_user(self)
        data = {
            'access': str(refresh.access_token)
        }
        return data
