from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAdminUser
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from .models import CustomUser, PasscodeGroup
from .serializers import CustomUserSerializer, ChangeAdminPasswordSerializer


# Single Login Endpoint for Both Admin & Guest
class LoginView(ObtainAuthToken):
    permission_classes = [AllowAny]  

    def get(self, request):
        return Response({"message": "Please login with Passcode"})


    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(
            data=request.data, 
            context={'request': request}
        )
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']

        # Check if user's passcode group is active (for guests only)
        if user.is_guest and (not user.passcode_group or not user.passcode_group.is_active):
            return Response(
                {"error": "This passcode is no longer active"},
                status=status.HTTP_403_FORBIDDEN
            )

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
            # Create a new passcode group
            new_group = PasscodeGroup.objects.create(
                name=f"Group {PasscodeGroup.objects.count() + 1}"
            )
            
            # Deactivate all previous passcode groups
            PasscodeGroup.objects.exclude(id=new_group.id).update(is_active=False)

            # Get or create guest user
            guest_user, created = CustomUser.objects.get_or_create(
                is_guest=True,
                defaults={'username': 'guest'}
            )

            # Update guest user with new credentials and group
            guest_user.passcode_group = new_group
            if 'username' in request.data:
                guest_user.username = request.data['username']
            if 'password' in request.data:
                guest_user.set_password(request.data['password'])
            guest_user.save()

            return Response({
                "message": "Guest user updated successfully",
                "group_name": new_group.name
            })
        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )


class ChangeAdminPasswordView(APIView):
    permission_classes = [IsAdminUser]  # Ensure only admins can access

    def put(self, request):
        serializer = ChangeAdminPasswordSerializer(data=request.data, context={'request': request})

        if serializer.is_valid():
            serializer.update(request.user, serializer.validated_data)
            return Response({"message": "Password updated successfully"}, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)