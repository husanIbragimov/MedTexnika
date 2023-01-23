from django.urls import path
from .views import AccountRegisterAPIView

urlpatterns = [
    path('register/', AccountRegisterAPIView.as_view()),
]
