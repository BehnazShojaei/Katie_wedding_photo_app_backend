from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from .models import Image
from .serializers import ImageSerializer
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from storages.backends.s3boto3 import S3Boto3Storage



class ImageListCreateView(APIView):

    permission_classes = [IsAuthenticated]  

    def get(self, request):
        if request.user.is_guest:
            # Guests can only see images from their active passcode group
            if request.user.passcode_group and request.user.passcode_group.is_active:
                images = Image.objects.filter(
                    passcode_group=request.user.passcode_group
                ).order_by('-uploaded_at')
            else:
                return Response(
                    {"error": "Invalid or inactive passcode group"},
                    status=status.HTTP_403_FORBIDDEN
                )
        else:
            # Admin can see all images
            images = Image.objects.all().order_by('-uploaded_at')
        
        serializer = ImageSerializer(images, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

    def post(self, request):


        try:
            # Get the image file from the request
            image_file = request.FILES.get('image')
            if not image_file:
                return Response({'error': 'No image file provided'}, status=status.HTTP_400_BAD_REQUEST)

            # Check if guest user has active passcode group
            if request.user.is_guest:
                if not request.user.passcode_group or not request.user.passcode_group.is_active:
                    return Response(
                        {"error": "Your passcode is no longer active!"},
                        status=status.HTTP_403_FORBIDDEN
                    )
                
        
         # Create the image data dictionary matching your model fields
            image_data = {
                'image': image_file,  
                'name': request.data.get('name', ''),
                'comment': request.data.get('comment', '')
                }


            # Serialize and save the image data
            serializer = ImageSerializer(data=image_data, context={'request': request})
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            print(f"Error uploading image: {str(e)}")
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ImageDetailView(APIView):
    
    permission_classes = [IsAuthenticated] 

    def get(self, request, pk):
        try:
            image = Image.objects.get(pk=pk)  # Manually fetching the image
            serializer = ImageSerializer(image)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Image.DoesNotExist:
            return Response(
                {"error": "Image not found"}, 
                status=status.HTTP_404_NOT_FOUND
            )
        
class ImageDeleteView(APIView):
    
    permission_classes = [IsAdminUser] 
    
    def delete(self, request, pk):
        try:
            image = Image.objects.get(pk=pk)
            image.delete()
            return Response(
                {"message": "Image deleted successfully"}, 
                status=status.HTTP_204_NO_CONTENT
            )
        except Image.DoesNotExist:
            return Response(
                {"error": "Image not found"}, 
                status=status.HTTP_404_NOT_FOUND
            ) 

@csrf_exempt
def test_upload(request):
    if request.method == 'POST' and request.FILES.get('test_file'):
        try:
            file = request.FILES['test_file']
            # Create S3 storage instance
            storage = S3Boto3Storage()
            # Save file with explicit media prefix
            file_name = storage.save(f'media/{file.name}', file)
            file_url = storage.url(file_name)
            
            print(f"Storage class: {storage.__class__.__name__}")
            print(f"File saved as: {file_name}")
            print(f"File URL: {file_url}")
            
            return JsonResponse({'message': 'Upload successful', 'url': file_url})
        except Exception as e:
            print(f"Error: {str(e)}")
            return JsonResponse({'error': str(e)}, status=500)
    return JsonResponse({'message': 'Please send a file'}, status=400)