from pytest_mock import MockerFixture
from rest_framework import status
from rest_framework.response import Response
from rest_framework.test import APIClient

from myinfo import serializers
from myinfo.api.exceptions import MyInfoAPIException, TokenNotProvidedAPIException
from myinfo.exceptions import MyInfoClientError


def test_auth_url(client: APIClient, mocker: MockerFixture):
    url = "http://google.com"
    mocker.patch("myinfo.utils.get_auth_url", return_value={"url": url})
    response: Response = client.get("/auth-url/", format="json")
    assert response.status_code == status.HTTP_200_OK
    assert response.data == {"url": url}


def test_receive_token(client: APIClient, mocker: MockerFixture):
    mocker.patch("myinfo.api.views.receive_access_token", return_value={"token": 1})
    response: Response = client.post(
        "/receive-token/",
        data={
            "token": "abc",
        },
        format="json",
    )
    assert response.status_code == status.HTTP_200_OK
    assert "token" in response.data


def test_receive_token_fails(client: APIClient):
    response: Response = client.post(
        "/receive-token/",
        format="json",
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "detail" in response.data
    assert response.data["detail"].code == TokenNotProvidedAPIException.default_code


def test_receive_token_client_error(client: APIClient, mocker: MockerFixture):
    mocker.patch("myinfo.api.views.receive_access_token", side_effect=MyInfoClientError)
    response: Response = client.post(
        "/receive-token/",
        data={
            "token": "abc",
        },
        format="json",
    )
    assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
    assert "detail" in response.data
    assert response.data["detail"].code == MyInfoAPIException.default_code


def test_me(client: APIClient, mocker: MockerFixture, person_test_data):
    serializer = serializers.PersonSerializer(person_test_data)
    mocker.patch(
        "myinfo.api.views.get_person",
        return_value=serializer.data,
    )
    response: Response = client.get(
        "/me/",
        data={
            "token": 1,
        },
        format="json",
    )
    assert response.status_code == status.HTTP_200_OK
    assert response.data == serializer.data
