from rest_framework import generics, status
from rest_framework.response import Response
from .serializers import RegisterSerializer

# REGISTER VIEW
class RegisterView(generics.GenericAPIView):
    serializer_class = RegisterSerializer
    permission_classes = []  # Allow anyone

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "User registered successfully"}, status=201)
        return Response(serializer.errors, status=400)


# LOGIN VIEW (Token-based)
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class LoginSerializer(TokenObtainPairSerializer):

    def validate(self, attrs):
        data = super().validate(attrs)

        # Standard fields
        data['user_id'] = self.user.id
        data['username'] = self.user.username
        data['email'] = self.user.email

        # Detect if user is a freelancer by checking Programmer model
        from marketplace.models import Programmer
        try:
            Programmer.objects.get(user=self.user)
            data['user_type'] = "freelancer"
        except Programmer.DoesNotExist:
            data['user_type'] = "client"

        return data




class LoginView(TokenObtainPairView):
    serializer_class = LoginSerializer
