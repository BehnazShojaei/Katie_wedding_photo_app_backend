from rest_framework import serializers
from .models import CustomUser
from django.contrib.auth import get_user_model


CustomUser = get_user_model()


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

class ChangeAdminPasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(write_only=True)
    new_password = serializers.CharField(write_only=True)

    def validate_old_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError("Old password is incorrect")
        return value

    def update(self, instance, validated_data):
        instance.set_password(validated_data['new_password'])  # Hash new password
        instance.save()
        return instance
