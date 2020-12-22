from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authentication import TokenAuthentication

from django.utils.translation import ugettext_lazy as _

from .serializers import UserSerializer, RegisterSerializer, LoginSerializer



# Register API
class RegisterAPI(generics.GenericAPIView):
    # NOTE: The token response is unique and PERMANENT for each user
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            "user": UserSerializer(user, context=self.get_serializer_context()).data,
            "token": token.key
        })


# Login API
class LoginAPI(ObtainAuthToken):
    # NOTE: The token response is unique and PERMANENT for each user

    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data
        token, created = Token.objects.get_or_create(user=user)

        return Response({
            "user": UserSerializer(user, context=self.get_serializer_context()).data,
            "token": token.key
        })

# LOGOUT 
class LogoutAPI(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)


    def get(self, request):
        self.request.user.auth_token.delete()
        return Response({"success": _("Successfully logged out.")},
                        status=status.HTTP_200_OK)



class ExampleUserAPI(APIView):
    
    authentication_classes = (TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):
        content = {'message': 'Hello, World!'}
        return Response(content)

    def get(self, request):
        content = {'message': 'Hello, World!'}
        return Response({"user": self.request.user.email})

