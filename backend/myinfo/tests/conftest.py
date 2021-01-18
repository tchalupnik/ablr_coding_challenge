from pytest import fixture
from rest_framework.test import APIClient


@fixture
def client() -> APIClient:
    api_client = APIClient()
    return api_client
