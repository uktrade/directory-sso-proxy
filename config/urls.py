from django.conf.urls import url, include

from config import settings
from proxy.api.views_user import (
    SessionUserAPIProxyView,
    LastLoginAPIProxyView,
    PasswordCheckAPIView
)
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
)
from proxy.healthcheck.views import (
    HealthCheckDatabaseAPIProxyView, PingAPIProxyView
)
from proxy.oauth2.views_user import UserRetrieveAPIProxyView
from proxy.oauth2.views import (
    AuthorizationProxyView,
    TokenProxyView,
    RevokeTokenProxyView
)
from proxy.utils import NotFoundProxyView, StaticProxyView, AdminProxyView
from testapi.views import UserByEmailAPIView

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
        r'^healthcheck/database/$',
        HealthCheckDatabaseAPIProxyView.as_view(),
        name="health_check_proxy"
    ),
    url(
        r'^healthcheck/ping/$',
        PingAPIProxyView.as_view(),
        name="ping_proxy"
    ),
    url(
        r'^session-user/$',
        SessionUserAPIProxyView.as_view(),
        name="session_user_proxy"
    ),
    url(
        r'^last-login/$',
        LastLoginAPIProxyView.as_view(),
        name="last_login_proxy"
    ),
    url(
        r'^password-check/$',
        PasswordCheckAPIView.as_view(),
        name='password_check'
    ),
]

urlpatterns = [
    url(
        r"^$",
        SSOLandingPageProxyView.as_view(),
        name="sso_root_proxy"
    ),
    url(
        r"^static/",
        StaticProxyView.as_view(),
        name="static_proxy"
    ),
    url(
        r"^admin/",
        AdminProxyView.as_view(),
        name="admin_proxy"
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

if settings.ENABLE_TEST_API:
    urlpatterns += [
        url(
            r'^testapi/user-by-email/(?P<email>.*)/$',
            UserByEmailAPIView.as_view(),
            name='user_by_email'
        )
    ]
