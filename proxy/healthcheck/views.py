from proxy.utils import CheckSignatureMixin, BaseProxyView


class HealthCheckAPIProxyView(BaseProxyView):
    pass


class PingAPIProxyView(CheckSignatureMixin, BaseProxyView):
    pass
