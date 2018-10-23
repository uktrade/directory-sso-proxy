from urllib.parse import urljoin

from django.utils.encoding import iri_to_uri


class UrlPrefixer:

    def __init__(self, request, prefix):
        self.prefix = prefix
        self.request = request

    @property
    def is_path_prefixed(self):
        return self.request.path.startswith(self.prefix)

    @property
    def path(self):
        canonical_path = urljoin(self.prefix, self.request.path.lstrip('/'))
        if not canonical_path.endswith('/'):
            canonical_path += '/'
        return canonical_path

    @property
    def full_path(self):
        path = self.path
        querystring = self.request.META.get('QUERY_STRING', '')
        if querystring:
            path += ('?' + iri_to_uri(querystring))
        return path
