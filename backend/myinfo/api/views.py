from django.utils.datastructures import MultiValueDictKeyError
from jwt import DecodeError, ExpiredSignatureError
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from ..exceptions import MyInfoClientError
from ..utils import get_auth_url, get_person, receive_access_token
from .exceptions import (
    ExpiredTokenAPIException,
    InvalidTokenAPIException,
    MyInfoAPIException,
    TokenNotProvidedAPIException,
)


class PersonView(APIView):
    def get(self, request: Request) -> Response:
        try:
            access_token = self.request.query_params["token"]
        except MultiValueDictKeyError:
            raise TokenNotProvidedAPIException

        try:
            person = get_person(access_token=access_token)
        except DecodeError:
            raise InvalidTokenAPIException
        except ExpiredSignatureError:
            raise ExpiredTokenAPIException

        return Response(person)


class ReceiveTokenAPIView(APIView):
    def post(self, request: Request) -> Response:
        try:
            token = request.data["token"]
        except KeyError:
            raise TokenNotProvidedAPIException

        try:
            access_token = receive_access_token(token=token)
        except MyInfoClientError:
            raise MyInfoAPIException

        return Response(access_token)


class AuthUrlAPIView(APIView):
    def get(self, request: Request) -> Response:
        url = get_auth_url()
        return Response(url)
