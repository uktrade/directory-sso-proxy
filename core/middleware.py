from urllib.parse import urljoin

from django.conf import settings
from django.shortcuts import redirect
from django.urls import resolve
from django.urls.exceptions import Resolver404


class PrefixUrlMixin:

    prefix = '/sso/'

    def process_request(self, request):
        if settings.FEATURE_URL_PREFIX_ENABLED:
            if not request.path.startswith(self.prefix):
                path = request.get_full_path().lstrip('/')
                url = urljoin(self.prefix, path)
                try:
                    resolve(url)
                except Resolver404:
                    pass
                else:
                    return redirect(url)
