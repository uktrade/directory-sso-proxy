from django.conf import settings

from revproxy.views import ProxyView


class BaseProxyView(ProxyView):
    upstream = settings.SSO_UPSTREAM
