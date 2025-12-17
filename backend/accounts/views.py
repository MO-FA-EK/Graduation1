from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from .serializers import RegisterSerializer, ChangePasswordSerializer
from marketplace.models import Programmer 

class RegisterView(generics.GenericAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CustomLoginSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        
        data['user_id'] = self.user.id
        data['username'] = self.user.username
        data['email'] = self.user.email
        
        if self.user.is_superuser:
            data['user_type'] = 'admin'
        else:
            try:
                Programmer.objects.get(user=self.user)
                data['user_type'] = 'freelancer'
            except Programmer.DoesNotExist:
                data['user_type'] = 'client'
            
        return data

class LoginView(TokenObtainPairView):
    serializer_class = CustomLoginSerializer

class ChangePasswordView(generics.GenericAPIView):
    serializer_class = ChangePasswordSerializer
    permission_classes = [IsAuthenticated]

    def put(self, request, *args, **kwargs):
        user = request.user
        serializer = self.get_serializer(data=request.data, context={'request': request})

        if serializer.is_valid():
            user.set_password(serializer.validated_data['new_password'])
            user.save()
            return Response({"message": "Password updated successfully"}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# ADMIN VIEWS
from django.contrib.auth.models import User
from .serializers import UserSerializer
from .permissions import IsSuperUser

class AdminUserListView(generics.ListAPIView):
    queryset = User.objects.all().select_related('programmer')
    serializer_class = UserSerializer
    permission_classes = [IsSuperUser]

class AdminDeleteUserView(generics.DestroyAPIView):
    queryset = User.objects.all()
    permission_classes = [IsSuperUser]
    lookup_field = 'id'