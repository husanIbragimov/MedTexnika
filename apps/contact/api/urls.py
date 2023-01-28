from django.urls import path
from .views import GetInTouchCreateAPIView, SubscribeCreateAPIView, LocationListAPIView

urlpatterns = [
    path('create/', GetInTouchCreateAPIView.as_view()),
    path('subscribe/', SubscribeCreateAPIView.as_view()),
    path('location/', LocationListAPIView.as_view())
]
