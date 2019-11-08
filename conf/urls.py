from django.conf.urls import url, include


import proxy.core.views
import proxy.healthcheck.views
import proxy.oauth2.views
import proxy.user.views
import proxy.utils


handler404 = proxy.utils.NotFoundProxyView.as_view()


allauth_urlpatterns = [
    url(
        r'^signup/$',
        proxy.user.views.SignupProxyView.as_view(),
        name='account_signup_proxy'
    ),
    url(
        r'^login/$',
        proxy.user.views.LoginProxyView.as_view(),
        name='account_login_proxy'
    ),
    url(
        r'^logout/$',
        proxy.user.views.LogoutProxyView.as_view(),
        name='account_logout_proxy'
    ),
    url(
        r'^inactive/$',
        proxy.user.views.AccountInactiveProxyView.as_view(),
        name='account_inactive_proxy'
    ),
    url(
        r'^confirm-email/$',
        proxy.user.views.EmailVerificationSentProxyView.as_view(),
        name='account_email_verification_sent_proxy'
    ),
    url(
        r'^confirm-email/(?P<key>[-:\w]+)/$',
        proxy.user.views.ConfirmEmailProxyView.as_view(),
        name='account_confirm_email_proxy'
    ),

    url(
        r'^password/set/$',
        proxy.user.views.PasswordSetProxyView.as_view(),
        name='account_set_password_proxy'
    ),
    url(
        r'^password/reset/$',
        proxy.user.views.PasswordResetProxyView.as_view(),
        name='account_reset_password_proxy'
    ),
    url(
        r'^password/change/$',
        proxy.user.views.PasswordChangeProxyView.as_view(),
        name='account_change_password_proxy'
    ),
    url(
        r'^password/reset/done/$',
        proxy.user.views.PasswordResetDoneProxyView.as_view(),
        name='account_reset_password_done_proxy'
    ),
    url(
        r'^password/reset/key/(?P<uidb36>[0-9A-Za-z]+)-(?P<key>.+)/$',
        proxy.user.views.PasswordResetFromKeyProxyView.as_view(),
        name='account_reset_password_from_key_proxy'
    ),
]

oauth2_provider_patterns = [
    url(
        r'^authorize/$',
        proxy.oauth2.views.AuthorizationProxyView.as_view(),
        name='authorize_proxy'
    ),
    url(
        r'^token/$',
        proxy.oauth2.views.TokenProxyView.as_view(),
        name='token_proxy'
    ),
    url(
        r'^revoke_token/$',
        proxy.oauth2.views.RevokeTokenProxyView.as_view(),
        name='revoke_token_proxy'
    ),
    url(
        r'^user-profile/v1/$',
        proxy.oauth2.views.UserProfileProxyView.as_view(),
        name='user-profile'
    ),

]

healthcheck_urlpatterns = [
    url(
        r'^healthcheck/$',
        proxy.healthcheck.views.HealthCheckAPIProxyView.as_view(),
        name='health_check_proxy'
    ),
    url(
        r'^healthcheck/ping/$',
        proxy.healthcheck.views.PingAPIProxyView.as_view(),
        name='ping_proxy'
    ),
]

urlpatterns = [
    url(
        r'^robots\.txt$',
        proxy.core.views.RobotsView.as_view(),
        name='robots_proxy'
    ),
    url(
        r'^sitemap\.xml$',
        proxy.core.views.SitemapView.as_view(),
        name='sitemap_proxy'
    ),
    url(
        r'^$',
        proxy.user.views.SSOLandingPageProxyView.as_view(),
        name='sso_root_proxy'
    ),
    url(
        r'^static/',
        proxy.utils.StaticProxyView.as_view(),
        name='static_proxy'
    ),
    url(
        r'^admin/',
        proxy.utils.AdminProxyView.as_view(),
        name='admin_proxy'
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
        include(healthcheck_urlpatterns)
    ),
]

urlpatterns = [
    url(
        r'^sso/',
        include(urlpatterns)
    )
]

urlpatterns += [
    url(
        r'^static/',
        proxy.utils.StaticProxyView.as_view(),
    ),
]


authbroker_urls = [
    url(
        r'^sso/admin/login/$',
        proxy.user.views.StaffSSOProxyLoginView.as_view(),
        name='sso view login'
    ),
    url(
        '^sso/auth/',
        proxy.user.views.StaffSSOProxyAuthView.as_view(),
        name='sso view auth'
        ),
]

urlpatterns = [url('^', include(authbroker_urls))] + urlpatterns
