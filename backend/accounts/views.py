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
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token

class LoginView(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        token = Token.objects.get(key=response.data["token"])
        return Response({
            "token": token.key,
            "user_id": token.user.id,
            "username": token.user.username,
            "email": token.user.email,
        })
