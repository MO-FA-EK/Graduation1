# accounts/views.py
from django.contrib.auth.models import User

from rest_framework import generics, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .serializers import RegisterSerializer, UserTokenObtainPairSerializer
from .throttles import LoginRateThrottle, RegisterRateThrottle


class RegisterView(generics.CreateAPIView):
    """
    POST /api/auth/register/
    """
    queryset = User.objects.all()
    permission_classes = [AllowAny]
    serializer_class = RegisterSerializer
    throttle_classes = [RegisterRateThrottle]


class LoginView(TokenObtainPairView):
    """
    POST /api/auth/login/
    Returns: { access, refresh, user: {id, username, email} }
    """
    serializer_class = UserTokenObtainPairSerializer
    throttle_classes = [LoginRateThrottle]


class TokenRefreshCustomView(TokenRefreshView):
    """
    POST /api/auth/refresh/
    Standard SimpleJWT refresh endpoint.
    """
    permission_classes = [AllowAny]


class ValidateTokenView(APIView):
    """
    GET /api/auth/validate-token/
    Checks if provided access token is valid.
    """
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
