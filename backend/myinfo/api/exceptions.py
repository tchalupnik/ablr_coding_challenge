from rest_framework.exceptions import APIException


class TokenNotProvidedAPIException(APIException):
    status_code = 400
    default_detail = "Token is not provided"
    default_code = "token_not_provided"


class InvalidTokenAPIException(APIException):
    status_code = 400
    default_detail = "Token is invalid"
    default_code = "invalid_token"


class ExpiredTokenAPIException(APIException):
    status_code = 400
    default_detail = "Token is expired"
    default_code = "expired_token"


class MyInfoAPIException(APIException):
    status_code = 500
    default_detail = "MyInfo integration error"
    default_code = "myinfo_error"
