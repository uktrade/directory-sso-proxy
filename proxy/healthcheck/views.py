from proxy.utils import CheckSignatureMixin, BaseProxyView


class HealthCheckAPIProxyView(CheckSignatureMixin, BaseProxyView):
    pass
