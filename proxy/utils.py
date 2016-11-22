from django.conf import settings

from revproxy.views import ProxyView


class BaseProxyView(ProxyView):

    upstream = settings.SSO_UPSTREAM

    def dispatch(self, request, *args, **kwargs):

        path = kwargs.get('path') or request.get_full_path()

        # revproxy requires the path to not start with a slash
        if path.startswith('/'):
            path = path[1:]

        return super(BaseProxyView, self).dispatch(request, path)
