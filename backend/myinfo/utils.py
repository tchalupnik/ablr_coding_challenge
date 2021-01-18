from myinfo import serializers
from requests import HTTPError

from .client import MyInfoClient
from .exceptions import MyInfoClientError
from .security import get_decoded_access_token, get_decrypted_person_data


def get_person(*, access_token: str) -> serializers.PersonSerializer:
    client = MyInfoClient()
    decoded_access_token = get_decoded_access_token(access_token)
    uinfin = decoded_access_token["sub"]
    response = client.get_person(uinfin=uinfin, access_token=access_token)
    data = get_decrypted_person_data(response)
    serializer = serializers.PersonSerializer(data)
    return serializer.data


def receive_access_token(*, token: str) -> serializers.ReceiveTokenSerializer:
    client = MyInfoClient()
    try:
        response = client.get_access_token(auth_code=token)
    except HTTPError as e:
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
