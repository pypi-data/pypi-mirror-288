import jwt
from datetime import datetime, timedelta
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from django.utils import timezone

from rest_framework.response import Response

# local imports
from .models import User

# create a service to handle token creation and verification
# which includes the following methods:
# 1. create access and refresh token
# 2. verify token
# 4. get token from request header
# 5. get token from request query string
# 6. get token from request authorization header
# 7. generate refresh token from access token


class JWTTokenHandler:

    @staticmethod
    def set_cookies_if_request_secured(request, access_token, refresh_token):
        """ set cookies if request is secured else send tokens in response body
        """
        response = Response()

        data = {'message': 'Login successful'}

        if request.is_secure():
            # set access token cookie
            response.set_cookie(
                'access_token', access_token, httponly=True, secure=True)

            # set refresh token cookie
            response.set_cookie(
                'refresh_token', refresh_token, httponly=True, secure=True)

            response.data = data

        # else send access and refresh token in response body
        else:
            response.data = {
                **data,
                'access_token': access_token,
                'refresh_token': refresh_token
            }
        return response

    @staticmethod
    def create_token(payload):
        # create token
        token = jwt.encode(
            payload, settings.SECRET_KEY, algorithm='HS256')

        return token

    @staticmethod
    def create_access_and_refresh_token(request, user):
        # create access token payload
        payload = {
            'user_id': str(user.id),
            'exp': datetime.utcnow() + timedelta(days=1),
            'iat': datetime.utcnow(),
            'email': user.email
        }

        # create access token
        access_token = JWTTokenHandler.create_token(payload)

        # create refresh token payload
        payload = {
            **payload,
            'exp': datetime.utcnow() + timedelta(days=7),
        }

        # create refresh token
        refresh_token = JWTTokenHandler.create_token(payload)

        return JWTTokenHandler.set_cookies_if_request_secured(request, access_token, refresh_token)

    @ staticmethod
    def verify_token(token):
        try:
            # verify token
            payload = jwt.decode(
                token, settings.SECRET_KEY, algorithms=['HS256'])

            # get user id from payload
            user_id = payload['user_id']

            user = User.objects.get(id=user_id)

            return user
        except jwt.ExpiredSignatureError:
            return None
        except jwt.InvalidTokenError:
            return None

    @ staticmethod
    def get_token_from_request_header(request):
        # get token from request header
        token = request.META.get('HTTP_AUTHORIZATION', None)

        return token

    @ staticmethod
    def get_token_from_request_query_string(request):
        # get token from request query string
        token = request.query_params.get('token', None)

        return token

    @ staticmethod
    def get_token_from_request_authorization_header(request):
        # get token from request authorization header
        token = request.META.get('HTTP_AUTHORIZATION', None)

        return token

    @ staticmethod
    def generate_refresh_token_from_access_token(access_token):
        # verify access token
        user = JWTTokenHandler.verify_token(access_token)

        # create refresh token payload
        payload = {
            'user_id': str(user.id),
            'exp': datetime.utcnow() + timedelta(days=7),
            'iat': datetime.utcnow(),
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'is_staff': user.is_staff,
            'is_superuser': user.is_superuser
        }

        # create refresh token
        refresh_token = jwt.encode(
            payload, settings.SECRET_KEY, algorithm='HS256')

        return refresh_token