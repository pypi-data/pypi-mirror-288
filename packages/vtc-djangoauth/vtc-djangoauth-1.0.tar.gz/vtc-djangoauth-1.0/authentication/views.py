
# create authentication based views iusing rest framework's model viewset

# 3rd party imports
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action

# add your local imports
from .serializers import AuthSerializer
from .models import User
from .services import JWTTokenHandler
from .permissions import PublicEndpoint


class ObtainAuthToken(APIView):
    serializer_class = AuthSerializer
    permission_classes = (PublicEndpoint,)  # disables permission

    def post(self, request, *args, **kwargs):
        email = request.data.get('email')
        password = request.data.get('password')

        # validate email and password
        if not email or not password:
            return Response(
                {'message': 'Email and password required'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # get user
        user = User.objects.filter(email=email).first()

        # validate user
        if not user.check_password(password):
            return Response(
                {'message': 'Invalid credentials'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # create access and refresh token
        return JWTTokenHandler.create_access_and_refresh_token(
            request, user)