from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAdminUser
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from .models import CustomUser
from .serializers import CustomUserSerializer, ChangeAdminPasswordSerializer


# Single Login Endpoint for Both Admin & Guest
class LoginView(ObtainAuthToken):
    permission_classes = [AllowAny]  

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(
            data=request.data, 
            context={'request': request}
        )
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']

        # Generate or get token
        token, created = Token.objects.get_or_create(user=user)

        return Response({
            "token": token.key,
            "user_id": user.id,
            "username": user.username,
            "is_guest": user.is_guest  
        }, status=status.HTTP_200_OK)
    

# Update Guest User Credentials only admin 
class UpdateGuestUserView(APIView):
    permission_classes = [IsAdminUser]  

    def put(self, request):
        try:
            guest_user = CustomUser.objects.get(is_guest=True)
        except CustomUser.DoesNotExist:
            return Response({"error": "Guest user not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = CustomUserSerializer(guest_user, data=request.data, partial=True)
        
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Guest user updated successfully"})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ChangeAdminPasswordView(APIView):
    permission_classes = [IsAdminUser]  # Ensure only admins can access

    def put(self, request):
        serializer = ChangeAdminPasswordSerializer(data=request.data, context={'request': request})

        if serializer.is_valid():
            serializer.update(request.user, serializer.validated_data)
            return Response({"message": "Password updated successfully"}, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)