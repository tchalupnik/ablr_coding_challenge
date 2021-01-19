import logging

from requests import HTTPError

from myinfo import serializers

from .client import MyInfoClient
from .exceptions import MyInfoClientError
from .security import get_decoded_access_token, get_decrypted_person_data

log = logging.getLogger(__name__)


def get_person(*, access_token: str) -> serializers.PersonSerializer:
    client = MyInfoClient()
    decoded_access_token = get_decoded_access_token(access_token)
    uinfin = decoded_access_token["sub"]
    try:
        response = client.get_person(uinfin=uinfin, access_token=access_token)
    except HTTPError as e:
        log.exception(e)
        raise MyInfoClientError(e)

    data = get_decrypted_person_data(response)
    serializer = serializers.PersonSerializer(data)
    return serializer.data


def receive_access_token(*, token: str) -> serializers.ReceiveTokenSerializer:
    client = MyInfoClient()
    try:
        response = client.get_access_token(auth_code=token)
    except HTTPError as e:
        log.exception(e)
        raise MyInfoClientError(e)

    access_token = response["access_token"]
    serializer = serializers.ReceiveTokenSerializer(
        {
            "token": access_token,
        }
    )
    return serializer.data


def get_auth_url() -> serializers.AuthoriseUrlSerializer:
    client = MyInfoClient()
    url = client.get_authorise_url("blah")
    serializer = serializers.AuthoriseUrlSerializer(
        {
            "url": url,
        }
    )
    return serializer.data
