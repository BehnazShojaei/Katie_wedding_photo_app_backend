from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAdminUser
from .models import Image
from .serializers import ImageSerializer
from django.conf import settings


class ImageListCreateView(APIView):
    """
    Allow guests with a passcode to upload and view images.
    """

    def get(self, request):
       
        passcode = request.headers.get("GUEST_PASSCODE")  
        if passcode != settings.GUEST_PASSCODE:
            return Response({"error": "Oh dear, this passcode? Surely you jest! Try again, good sir/madam. 🍷"}, status=status.HTTP_403_FORBIDDEN)
        
        images = Image.objects.all()
        serializer = ImageSerializer(images, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
       
        passcode = request.headers.get("GUEST_PASSCODE")
        if passcode != settings.GUEST_PASSCODE:
            return Response({"error": "Oh dear, this passcode? Surely you jest! Try again, good sir/madam. 🍷"}, status=status.HTTP_403_FORBIDDEN)
        
        serializer = ImageSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ImageDeleteView(APIView):
    """
    Only superusers can delete images.
    """
    permission_classes = [IsAdminUser]  

    def delete(self, request, pk):
        try:
            image = Image.objects.get(pk=pk)
        except Image.DoesNotExist:
            return Response({"error": "Image not found"}, status=status.HTTP_404_NOT_FOUND)
        
        image.delete()
        return Response({"message": "Image deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
