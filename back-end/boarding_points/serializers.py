from rest_framework import serializers
from .models import BoardingPoint

class BoardingPointSerializer(serializers.ModelSerializer):
    class Meta:
        model = BoardingPoint
        fields = ['id', 'name', 'address_reference', 'route_order']