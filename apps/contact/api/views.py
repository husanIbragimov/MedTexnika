from rest_framework import generics
from apps.contact.models import GetInTouch, Subscribe, Location
from .serializers import GetInTouchSerializer, SubscribeSerializer, LocationSerializer


class GetInTouchCreateAPIView(generics.CreateAPIView):
    queryset = GetInTouch.objects.all()
    serializer_class = GetInTouchSerializer


class SubscribeCreateAPIView(generics.CreateAPIView):
    queryset = Subscribe.objects.filter(is_active=True).order_by('-id')
    serializer_class = SubscribeSerializer


class LocationListAPIView(generics.ListAPIView):
    queryset = Location.objects.all()
    serializer_class = LocationSerializer

