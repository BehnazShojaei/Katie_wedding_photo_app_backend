from rest_framework import serializers
from .models import CustomUser

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['username', 'password', 'is_guest']
        extra_kwargs = {
            'password': {'write_only': True},  
            'is_guest': {'read_only': True}    
        }

    def create(self, validated_data):
        user = CustomUser.objects.create_user(**validated_data)
        return user
    
    
    def update(self, instance, validated_data):
        if 'password' in validated_data:
            instance.set_password(validated_data.pop('password'))  # Hash password properly
            for attr, value in validated_data.items():
                setattr(instance, attr, value)
                instance.save()  # Explicitly save the updated instance
                return instance
