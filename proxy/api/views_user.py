from proxy.utils import BaseProxyView, CheckSignatureMixin


class SessionUserAPIProxyView(CheckSignatureMixin, BaseProxyView):
    pass


class LastLoginAPIProxyView(CheckSignatureMixin, BaseProxyView):
    pass


class PasswordCheckAPIView(CheckSignatureMixin, BaseProxyView):
    pass


class UserByEmailAPIView(CheckSignatureMixin, BaseProxyView):
    pass
