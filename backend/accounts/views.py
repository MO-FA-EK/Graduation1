from django.contrib.auth.models import User
from rest_framework import generics, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .serializers import RegisterSerializer, UserTokenObtainPairSerializer
from .throttles import LoginRateThrottle, RegisterRateThrottle

# ✅ Import the Freelancer Model from the other app
from marketplace.models import User as FreelancerProfile 

class RegisterView(generics.CreateAPIView):
    """
    POST /api/auth/register/
    """
    queryset = User.objects.all()
    permission_classes = [AllowAny]
    serializer_class = RegisterSerializer
    throttle_classes = [RegisterRateThrottle]

    def create(self, request, *args, **kwargs):
        # 1. Validate basic data (Name, Email, Password)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        # 2. Save the Basic User (for Login)
        user = serializer.save()

        # 3. Check the User Type coming from the Frontend
        user_type = request.data.get('user_type', 'client')

        # ✅ If it is a Freelancer, create an extra profile for them
        if user_type == 'freelancer':
            try:
                FreelancerProfile.objects.create(
                    name=user.username,
                    email=user.email,
                    category=request.data.get('category', 'General'),
                    skills=request.data.get('skills', ''),
                    experience_level=request.data.get('experience_level', 'Beginner'),
                    bio=request.data.get('description', ''),
                    portfolio=request.data.get('portfolio', ''),
                    # Handle image (if present)
                    image=request.FILES.get('image') 
                )
            except Exception as e:
                # If profile creation fails, delete the user account to avoid incomplete data
                user.delete()
                return Response(
                    {"error": f"Failed to create freelancer profile: {str(e)}"},
                    status=status.HTTP_400_BAD_REQUEST
                )

        # Return success message
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class LoginView(TokenObtainPairView):
    serializer_class = UserTokenObtainPairSerializer
    throttle_classes = [LoginRateThrottle]


class TokenRefreshCustomView(TokenRefreshView):
    permission_classes = [AllowAny]


class ValidateTokenView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        return Response(
            {
                "valid": True,
                "user": {
                    "id": user.id,
                    "username": user.username,
                    "email": user.email or "",
                },
            },
            status=status.HTTP_200_OK,
        )