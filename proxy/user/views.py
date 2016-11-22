from proxy.utils import BaseProxyView


class SignupProxyView(BaseProxyView):
    pass


class LoginProxyView(BaseProxyView):
    pass


class LogoutProxyView(BaseProxyView):
    pass


class PasswordResetProxyView(BaseProxyView):
    pass


class ConfirmEmailProxyView(BaseProxyView):
    pass


class PasswordResetFromKeyProxyView(BaseProxyView):
    pass


class SSOLandingPageProxyView(BaseProxyView):
    pass


class AccountInactiveProxyView(BaseProxyView):
    pass


class EmailVerificationSentProxyView(BaseProxyView):
    pass


class PasswordSetProxyView(BaseProxyView):
    pass


class PasswordChangeProxyView(BaseProxyView):
    pass


class PasswordResetDoneProxyView(BaseProxyView):
    pass


class NotFoundProxyView(BaseProxyView):
    """Redirects 404 to SSO in order to retrieve user context."""

    def dispatch(self, request, *args, **kwargs):

        # All requests reaching this view get the path rewritten to '404/'
        return super(NotFoundProxyView, self).dispatch(request, path='404/')
