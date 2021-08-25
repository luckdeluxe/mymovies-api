from django.contrib.auth import authenticate, login, logout
from rest_framework.response import Response
from rest_framework import status, generics
from rest_framework.views import APIView
from .serializers import UserSerializer

from django.dispatch import receiver
from django_rest_passwordreset.signals import reset_password_token_created


class LoginView(APIView):
    def post(self, request):
        #We recover the credentials and authenticate the user
        email = request.data.get('email', None)
        password = request.data.get('password', None)
        user = authenticate(email=email, password=password)

        #If it is correct we add the session information to the request
        if user:
            login(request, user)
            #We return the serialized user object to json
            return Response(UserSerializer(user).data, status=status.HTTP_200_OK)

        #If it is not correct we return an error in the request
        return Response(status=status.HTTP_404_NOT_FOUND)
        

class LogoutView(APIView):
    def post(self, request):
        # We delete the session information from the request
        logout(request)
        return Response(status=status.HTTP_200_OK)


class SignupView(generics.CreateAPIView):
    serializer_class = UserSerializer



@receiver(reset_password_token_created)
def password_reset_token_created(sender, instance, reset_password_token, *args, **kwargs):
    # Aquí deberíamos mandar un correo al cliente...
    print(
        f"\nRecupera la contraseña del correo '{reset_password_token.user.email}' usando el token '{reset_password_token.key}' desde la API http://localhost:8000/api/auth/reset/confirm/.")
    