from rest_framework import serializers
from .models import Car, Fueling, Accessory
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)  # Add a password field, make it write-only

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password')
    
    def create(self, validated_data):
      user = User.objects.create_user(
          username=validated_data['username'],
          email=validated_data['email'],
          password=validated_data['password']  # Ensures the password is hashed correctly
      )
      
      return user

class AccessorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Accessory
        fields = '__all__'

class CarSerializer(serializers.ModelSerializer):
    # fueled_for_today = serializers.SerializerMethodField()
    accessories = AccessorySerializer(many=True, read_only=True)
    user = serializers.PrimaryKeyRelatedField(read_only=True)

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