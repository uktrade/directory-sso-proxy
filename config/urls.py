from django.conf.urls import url, include

from proxy.api.views_user import SessionUserAPIProxyView
from proxy.user.views import (
    AccountInactiveProxyView,
    EmailVerificationSentProxyView,
    PasswordSetProxyView,
    PasswordChangeProxyView,
    PasswordResetDoneProxyView,
    ConfirmEmailProxyView,
    LoginProxyView,
    LogoutProxyView,
    PasswordResetFromKeyProxyView,
    SSOLandingPageProxyView,
    SignupProxyView,
    PasswordResetProxyView,
    NotFoundProxyView,
)
from proxy.healthcheck.views import HealthCheckAPIProxyView
from proxy.oauth2.views_user import UserRetrieveAPIProxyView
from proxy.oauth2.views import (
    AuthorizationProxyView,
    TokenProxyView,
    RevokeTokenProxyView
)


handler404 = NotFoundProxyView.as_view()

allauth_urlpatterns = [
    url(
        r"^signup/$",
        SignupProxyView.as_view(),
        name="account_signup_proxy"
    ),
    url(
        r"^login/$",
        LoginProxyView.as_view(),
        name="account_login_proxy"
    ),
    url(
        r"^logout/$",
        LogoutProxyView.as_view(),
        name="account_logout_proxy"
    ),
    url(
        r"^inactive/$",
        AccountInactiveProxyView.as_view(),
        name="account_inactive_proxy"
    ),
    url(
        r"^confirm-email/$",
        EmailVerificationSentProxyView.as_view(),
        name="account_email_verification_sent_proxy"
    ),
    url(
        r"^confirm-email/(?P<key>[-:\w]+)/$",
        ConfirmEmailProxyView.as_view(),
        name="account_confirm_email_proxy"
    ),

    url(
        r"^password/set/$",
        PasswordSetProxyView.as_view(),
        name="account_set_password_proxy"
    ),
    url(
        r"^password/reset/$",
        PasswordResetProxyView.as_view(),
        name="account_reset_password_proxy"
    ),
    url(
        r"^password/change/$",
        PasswordChangeProxyView.as_view(),
        name="account_change_password_proxy"
    ),
    url(
        r"^password/reset/done/$",
        PasswordResetDoneProxyView.as_view(),
        name="account_reset_password_done_proxy"
    ),
    url(
        r"^password/reset/key/(?P<uidb36>[0-9A-Za-z]+)-(?P<key>.+)/$",
        PasswordResetFromKeyProxyView.as_view(),
        name="account_reset_password_from_key_proxy"
    ),
]

oauth2_provider_patterns = [
    url(
        r'^user-profile/v1/$',
        UserRetrieveAPIProxyView.as_view(),
        name="user_profile_proxy"
    ),
    url(
        r'^authorize/$',
        AuthorizationProxyView.as_view(),
        name="authorize_proxy"
    ),
    url(
        r'^token/$',
        TokenProxyView.as_view(),
        name="token_proxy"
    ),
    url(
        r'^revoke_token/$',
        RevokeTokenProxyView.as_view(),
        name="revoke_token_proxy"
    ),
]

api_urlpatterns = [
    url(
        r'^$',
        HealthCheckAPIProxyView.as_view(),
        name="health_check_proxy"
    ),
    url(
        r'^session-user/$',
        SessionUserAPIProxyView.as_view(),
        name="session_user_proxy"
    ),
]

urlpatterns = [
    url(
        r"^",
        include('directory_constants.urls', namespace='constants')
    ),
    url(
        r"^$",
        SSOLandingPageProxyView.as_view(),
        name="sso_root_proxy"
    ),
    url(
        r'^accounts/',
        include(allauth_urlpatterns)
    ),
    url(
        r'^oauth2/',
        include(oauth2_provider_patterns, namespace='oauth2_provider_proxy')
    ),
    url(
        r'^api/v1/',
        include(api_urlpatterns)
    ),
]
