from rest_framework import serializers
from apps.contact.models import GetInTouch, Subscribe, Location


class GetInTouchSerializer(serializers.ModelSerializer):
    class Meta:
        model = GetInTouch
        fields = ['id',
                  'full_name',
                  'phone',
                  'email',
                  'message',
                  'user_data',
                  ]


class SubscribeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscribe
        fields = ['id', 'email']


class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = '__all__'
