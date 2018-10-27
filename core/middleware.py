from directory_components.middleware import AbstractPrefixUrlMiddleware


class PrefixUrlMiddleware(AbstractPrefixUrlMiddleware):
    prefix = '/sso/'

    def process_request(self, request):
        if request.path.startswith('/static/'):
            return
        return super().process_request(request)
