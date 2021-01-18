import logging
from json import JSONDecodeError
from urllib.parse import quote, urlencode

import requests
from myinfo import settings
from myinfo.security import generate_authorization_header

log = logging.getLogger(__name__)


class MyInfoClient(object):
    """
    See API doc at https://public.cloud.myinfo.gov.sg/myinfo/api/myinfo-kyc-v3.1.1.html
    Test data: https://www.ndi-api.gov.sg/library/trusted-data/myinfo/resources-personas.
    """

    API_TIMEOUT = 30

    def __init__(self):
        """
        Initialize a request session to interface with remote API
        """
        self.session = requests.Session()

    def request(
        self, api_url, method="GET", auth_header=None, params=None, data=None, json=None
    ):
        """
        Returns:
            dict or str

        Raises:
            requests.RequestException
        """
        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
            "Cache-Control": "no-cache",
        }
        if auth_header:
            headers["Authorization"] = auth_header

        log.info("headers = %s", headers)
        response = self.session.request(
            method,
            url=api_url,
            params=params,
            data=data,
            timeout=self.API_TIMEOUT,
            verify=settings.CERT_VERIFY,
            headers=headers,
        )

        response.raise_for_status()

        try:
            return response.json()
        except JSONDecodeError:
            return response.text

    def get_access_token(self, auth_code: str, callback_url: str = None):
        """
        Generate an access token when presented with a valid authcode obtained from the Authorise API.
        This token can then be used to request for the user's data that were consented.

        """
        # At the moment, only this URL is whitelisted as we're using key from MyInfo demo app
        # https://github.com/ndi-trusted-data/myinfo-demo-app
        # Otherwise, we would get this error:
        # `redirect_uri_mismatch The redirection URI provided does not match a pre-registered value.`
        if not callback_url:
            callback_url = "http://localhost:3001/callback"

        api_url = f"{settings.MYINFO_ROOT}/token"
        params = {
            "client_id": settings.MYINFO_CLIENT_ID,
            "client_secret": settings.MYINFO_SECRET,
            "code": auth_code,
            "grant_type": "authorization_code",
            "redirect_uri": callback_url,
        }
        auth_header = generate_authorization_header(
            url=api_url, params=params, method="POST", app_id=settings.MYINFO_CLIENT_ID
        )
        log.info("auth_header: %s", auth_header)

        resp = self.request(
            api_url, method="POST", auth_header=auth_header, data=params
        )

        return resp

    def get_person(self, uinfin, access_token):
        """
        Return user's data from MyInfo when presented with a valid access token obtained from the Token API.
        """
        api_url = f"{settings.MYINFO_ROOT}/person/{uinfin}/"
        params = {
            "client_id": settings.MYINFO_CLIENT_ID,
            "attributes": settings.MYINFO_ATTRS,
        }
        auth_header = generate_authorization_header(
            url=api_url, params=params, method="GET", app_id=settings.MYINFO_CLIENT_ID
        )

        auth_header += f",Bearer {access_token}"
        log.info("auth_header: %s", auth_header)

        resp = self.request(
            api_url, method="GET", auth_header=auth_header, params=params
        )

        return resp

    @staticmethod
    def get_authorise_url(state, callback_url: str = None):
        """
        Return a redirect URL to SingPass login page for user's authentication and consent.
        """
        # At the moment, only this URL is whitelisted as we're using key from MyInfo demo app
        # https://github.com/ndi-trusted-data/myinfo-demo-app
        # Otherwise, we would get this error:
        # `redirect_uri_mismatch The redirection URI provided does not match a pre-registered value.`
        if not callback_url:
            callback_url = "http://localhost:3001/callback"

        query = {
            "client_id": settings.MYINFO_CLIENT_ID,
            "attributes": settings.MYINFO_ATTRS,
            "purpose": "credit risk assessment",
            "state": state,
            "redirect_uri": callback_url,
        }
        querystring = urlencode(query, safe=",/:", quote_via=quote)
        authorise_url = f"{settings.MYINFO_ROOT}/authorise?{querystring}"
        return authorise_url
