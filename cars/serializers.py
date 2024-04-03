from rest_framework import serializers
from .models import Car, Fueling

class CarSerializer(serializers.ModelSerializer):
    fueled_for_today = serializers.SerializerMethodField()
    class Meta:
        model = Car
        fields = '__all__'

        def get_fueled_for_today(self, obj):
            return obj.fueled_for_today()

class FuelingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Fueling
        fields = '__all__'
        read_only_field = ('car',)