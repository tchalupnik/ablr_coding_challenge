from myinfo import serializers
from myinfo.api.exceptions import TokenNotProvidedAPIException
from pytest_mock import MockerFixture
from rest_framework import status
from rest_framework.response import Response
from rest_framework.test import APIClient


def test_auth_url(client: APIClient, mocker: MockerFixture):
    url = "http://google.com"
    mocker.patch("myinfo.utils.get_auth_url", return_value=url)
    response: Response = client.get("/auth-url/", format="json")
    assert response.status_code == status.HTTP_200_OK
    assert response.data == {"url": url}


def test_receive_token(client: APIClient, mocker: MockerFixture):
    mocker.patch("myinfo.utils.receive_access_token", return_value=1)
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


def test_me(client: APIClient, mocker: MockerFixture):
    serializer = serializers.PersonSerializer(
        {
            "uinfin": {
                "lastupdated": "2020-10-01",
                "source": "1",
                "classification": "C",
                "value": "S3100052A",
            },
            "name": {
                "lastupdated": "2020-10-01",
                "source": "1",
                "classification": "C",
                "value": "TAN HENG HUAT",
            },
            "sex": {
                "lastupdated": "2020-10-01",
                "code": "F",
                "source": "1",
                "classification": "C",
                "desc": "FEMALE",
            },
            "race": {
                "lastupdated": "2020-10-01",
                "code": "CN",
                "source": "1",
                "classification": "C",
                "desc": "CHINESE",
            },
            "nationality": {
                "lastupdated": "2020-10-01",
                "code": "SG",
                "source": "1",
                "classification": "C",
                "desc": "SINGAPORE CITIZEN",
            },
            "dob": {
                "lastupdated": "2020-10-01",
                "source": "1",
                "classification": "C",
                "value": "1998-06-06",
            },
            "email": {
                "lastupdated": "2020-10-01",
                "source": "2",
                "classification": "C",
                "value": "myinfotesting@gmail.com",
            },
            "mobileno": {
                "lastupdated": "2020-10-01",
                "source": "2",
                "classification": "C",
                "areacode": {"value": "65"},
                "prefix": {"value": "+"},
                "nbr": {"value": "97399245"},
            },
            "regadd": {
                "country": {"code": "SG", "desc": "SINGAPORE"},
                "unit": {"value": "128"},
                "street": {"value": "BEDOK NORTH AVENUE 4"},
                "lastupdated": "2020-10-01",
                "block": {"value": "102"},
                "postal": {"value": "460102"},
                "source": "1",
                "classification": "C",
                "floor": {"value": "09"},
                "type": "SG",
                "building": {"value": "PEARL GARDEN"},
            },
            "housingtype": {
                "lastupdated": "2020-10-01",
                "code": "",
                "source": "1",
                "classification": "C",
                "desc": "",
            },
            "hdbtype": {
                "lastupdated": "2020-10-01",
                "code": "113",
                "source": "1",
                "classification": "C",
                "desc": "3-ROOM FLAT (HDB)",
            },
            "marital": {
                "lastupdated": "2020-10-01",
                "code": "2",
                "source": "1",
                "classification": "C",
                "desc": "MARRIED",
            },
            "edulevel": {
                "lastupdated": "2020-10-01",
                "code": "",
                "source": "2",
                "classification": "C",
                "desc": "",
            },
            "ownerprivate": {
                "lastupdated": "2020-10-01",
                "source": "1",
                "classification": "C",
                "value": False,
            },
            "cpfcontributions": {
                "lastupdated": "2020-10-01",
                "history": [
                    {
                        "date": {"value": "2019-07-30"},
                        "employer": {"value": "CRYSTAL HORSE INVEST PTE LTD"},
                        "amount": {"value": 1425},
                        "month": {"value": "2019-07"},
                    },
                    {
                        "date": {"value": "2019-08-30"},
                        "employer": {"value": "CRYSTAL HORSE INVEST PTE LTD"},
                        "amount": {"value": 1425},
                        "month": {"value": "2019-08"},
                    },
                    {
                        "date": {"value": "2019-09-30"},
                        "employer": {"value": "CRYSTAL HORSE INVEST PTE LTD"},
                        "amount": {"value": 2850},
                        "month": {"value": "2019-09"},
                    },
                    {
                        "date": {"value": "2019-10-30"},
                        "employer": {"value": "CRYSTAL HORSE INVEST PTE LTD"},
                        "amount": {"value": 1425},
                        "month": {"value": "2019-10"},
                    },
                    {
                        "date": {"value": "2019-11-30"},
                        "employer": {"value": "CRYSTAL HORSE INVEST PTE LTD"},
                        "amount": {"value": 1425},
                        "month": {"value": "2019-11"},
                    },
                    {
                        "date": {"value": "2019-12-30"},
                        "employer": {"value": "CRYSTAL HORSE INVEST PTE LTD"},
                        "amount": {"value": 1425},
                        "month": {"value": "2019-12"},
                    },
                    {
                        "date": {"value": "2020-01-30"},
                        "employer": {"value": "CRYSTAL HORSE INVEST PTE LTD"},
                        "amount": {"value": 5700},
                        "month": {"value": "2020-01"},
                    },
                    {
                        "date": {"value": "2020-02-29"},
                        "employer": {"value": "CRYSTAL HORSE INVEST PTE LTD"},
                        "amount": {"value": 1575},
                        "month": {"value": "2020-02"},
                    },
                    {
                        "date": {"value": "2020-03-30"},
                        "employer": {"value": "CRYSTAL HORSE INVEST PTE LTD"},
                        "amount": {"value": 1575},
                        "month": {"value": "2020-03"},
                    },
                    {
                        "date": {"value": "2020-04-30"},
                        "employer": {"value": "CRYSTAL HORSE INVEST PTE LTD"},
                        "amount": {"value": 1575},
                        "month": {"value": "2020-04"},
                    },
                    {
                        "date": {"value": "2020-05-30"},
                        "employer": {"value": "CRYSTAL HORSE INVEST PTE LTD"},
                        "amount": {"value": 1575},
                        "month": {"value": "2020-05"},
                    },
                    {
                        "date": {"value": "2020-06-30"},
                        "employer": {"value": "CRYSTAL HORSE INVEST PTE LTD"},
                        "amount": {"value": 1575},
                        "month": {"value": "2020-06"},
                    },
                    {
                        "date": {"value": "2020-07-30"},
                        "employer": {"value": "CRYSTAL HORSE INVEST PTE LTD"},
                        "amount": {"value": 1575},
                        "month": {"value": "2020-07"},
                    },
                    {
                        "date": {"value": "2020-08-30"},
                        "employer": {"value": "CRYSTAL HORSE INVEST PTE LTD"},
                        "amount": {"value": 1575},
                        "month": {"value": "2020-08"},
                    },
                    {
                        "date": {"value": "2020-09-30"},
                        "employer": {"value": "CRYSTAL HORSE INVEST PTE LTD"},
                        "amount": {"value": 3150},
                        "month": {"value": "2020-09"},
                    },
                ],
                "source": "1",
                "classification": "C",
            },
            "cpfbalances": {
                "lastupdated": "2020-10-01",
                "oa": {"value": 58839.75},
                "source": "1",
                "ma": {"value": 20466},
                "classification": "C",
                "sa": {"value": 15349.5},
            },
            "birthcountry": {
                "lastupdated": "2020-10-01",
                "code": "SG",
                "source": "1",
                "classification": "C",
                "desc": "SINGAPORE",
            },
            "residentialstatus": {
                "lastupdated": "2020-10-01",
                "code": "C",
                "source": "1",
                "classification": "C",
                "desc": "Citizen",
            },
            "aliasname": {
                "lastupdated": "2020-10-01",
                "source": "1",
                "classification": "C",
                "value": "TRICIA TAN XIAO HUI",
            },
            "marriedname": {
                "lastupdated": "2020-10-01",
                "source": "1",
                "classification": "C",
                "value": "",
            },
            "passtype": {
                "lastupdated": "2020-10-01",
                "code": "",
                "source": "3",
                "classification": "C",
                "desc": "",
            },
            "employmentsector": {
                "lastupdated": "2020-10-01",
                "source": "3",
                "classification": "C",
                "value": "",
            },
            "noahistory": {
                "noas": [
                    {
                        "amount": {"value": 64400},
                        "trade": {"value": 0},
                        "interest": {"value": 0},
                        "taxclearance": {"value": "N"},
                        "yearofassessment": {"value": "2019"},
                        "employment": {"value": 64400},
                        "category": {"value": "ORIGINAL"},
                        "rent": {"value": 0},
                    },
                    {
                        "amount": {"value": 53700},
                        "trade": {"value": 0},
                        "interest": {"value": 0},
                        "taxclearance": {"value": "N"},
                        "yearofassessment": {"value": "2018"},
                        "employment": {"value": 36112.8},
                        "category": {"value": "ORIGINAL"},
                        "rent": {"value": 0},
                    },
                ],
                "lastupdated": "2020-10-01",
                "source": "1",
                "classification": "C",
            },
        }
    )
    mocker.patch(
        "myinfo.utils.get_person",
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