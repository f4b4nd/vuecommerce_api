from rest_framework import generics, permissions, status
from rest_framework.response import Response
# from knox.models import AuthToken
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token

from .serializers import UserSerializer, RegisterSerializer, LoginSerializer



# Register API
class RegisterAPI(generics.GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        # _, token = AuthToken.objects.create(user)
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            "user": UserSerializer(user, context=self.get_serializer_context()).data,
            "token": token.key
        })

# from knox.views import LoginView as KnoxLoginView
# from rest_framework.authentication import BasicAuthentication
# class LoginView(KnoxLoginView):
    # Need to override knoxloginView as it's the only only default authentication class (cf. doc)
    # authentication_classes = [BasicAuthentication]

# Login API
from rest_framework.authtoken.views import ObtainAuthToken
class LoginAPI(ObtainAuthToken):
    # authentication_classes = ()
    # permission_classes = (permissions.AllowAny,)
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data
        # token = Token.objects.create(user=user)
        token, created = Token.objects.get_or_create(user=user)

        return Response({
            "user": UserSerializer(user, context=self.get_serializer_context()).data,
            "token": token.key
        })

class LogoutAPI(APIView):
    def get(self, request, format=None):
        # simply delete the token to force a login
        request.user.auth_token.delete()
        return Response(status=status.HTTP_200_OK)

# Get user API
# from knox.auth import TokenAuthentication

from rest_framework.authentication import TokenAuthentication
# class UserAPI(generics.RetrieveAPIView):
class UserAPI(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = UserSerializer

    def post(self, request):
        content = {'message': 'Hello, World!'}
        return Response({"user": self.request.user.auth_token.key})

    def get(self, request):
        content = {'message': 'Hello, World!'}
        return Response({"user": self.request.user.email})

    def get_object(self):
        return self.request.user
