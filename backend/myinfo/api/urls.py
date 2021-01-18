from django.urls import path
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.views import APIView

from . import views


class RootView(APIView):
    """
    Order of things:
    1. Get auth url from /auth-url/ endpoint
    2. Authorize using that url
    3. Get access token from /retrieve-token/ endpoint providing token in data from point 1
    4. Get personal details from /me/ providing access token in query params from point 3
    """

    def get(self, request):
        urls = [
            ("auth_url", reverse("auth-url", request=request)),
            ("receive_token", reverse("receive-token", request=request)),
            ("me", reverse("me", request=request)),
        ]
        return Response(urls)


urlpatterns = [
    path("", RootView.as_view()),
    path("auth-url/", views.AuthUrlAPIView.as_view(), name="auth-url"),
    path("receive-token/", views.ReceiveTokenAPIView.as_view(), name="receive-token"),
    path("me/", views.PersonView.as_view(), name="me"),
]
