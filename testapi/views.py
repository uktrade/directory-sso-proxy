from proxy.utils import BaseProxyView, CheckSignatureMixin


class UserByEmailAPIView(CheckSignatureMixin, BaseProxyView):
    pass
