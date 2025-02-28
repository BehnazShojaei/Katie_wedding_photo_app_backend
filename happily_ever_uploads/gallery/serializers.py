from rest_framework import serializers
from .models import Image

class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ['id', 'image', 'name', 'comment', 'uploaded_at', 'uploaded_by', 'passcode_group']
        read_only_fields = ['uploaded_at', 'uploaded_by', 'passcode_group']  


    def create(self, validated_data):
        request = self.context.get('request')
        if request and hasattr(request, "user"):
            validated_data['uploaded_by'] = request.user  
            if request.user.is_guest and hasattr(request.user, 'passcode_group'):
                validated_data['passcode_group'] = request.user.passcode_group

        return super().create(validated_data)
