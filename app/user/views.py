from rest_framework import generics, authentication, permissions
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings

from .serializers import UserSerializer, AuthTokenSerializer


class CreateUserView(generics.CreateAPIView):
    serializer_class = UserSerializer


class CreateTokenView(ObtainAuthToken):
    serializer_class = AuthTokenSerializer
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES
    # This is required to enable the view in the browsable API


class ManageUserView(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    authentication_classes = (
        authentication.TokenAuthentication,)
    # This is required to make sure the user is authenticated

    permission_classes = (
        permissions.IsAuthenticated,)

    # This is required to make sure the user is authenticated

    def get_object(self):
        return self.request.user
        # This is the user object that is authenticated
