from django.urls import path, include
from rest_framework_simplejwt.views import (
    token_blacklist,
    token_obtain_pair,
    token_refresh,
    token_verify,
)

from accounts.views import RegisterView, PublicUserProfileView

urlpatterns = [
    path("register/", RegisterView.as_view(), name="jwt-register"),
    path("login/", token_obtain_pair, name="jwt-obtain"),
    path("refresh/", token_refresh, name="jwt-refresh"),
    path("revoke/", token_blacklist, name="jwt-revoke"),
    path("verify/", token_verify, name="jwt-verify"),
    path("profile/", PublicUserProfileView.as_view(), name="profile"),
]
