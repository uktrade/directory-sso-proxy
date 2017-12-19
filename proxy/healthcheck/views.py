from proxy.utils import CheckSignatureMixin, BaseProxyView


class HealthCheckDatabaseAPIProxyView(BaseProxyView):
    pass


class PingAPIProxyView(CheckSignatureMixin, BaseProxyView):
    pass
