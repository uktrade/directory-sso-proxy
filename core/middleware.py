from django.conf import settings
from django.shortcuts import redirect
from django.urls import resolve
from django.urls.exceptions import Resolver404

from core import helpers


class PrefixUrlMiddleware:

    prefix = '/sso/'

    def process_request(self, request):
        if settings.FEATURE_URL_PREFIX_ENABLED:
            prefixer = helpers.UrlPrefixer(request=request, prefix=self.prefix)
            if not prefixer.is_path_prefixed:
                try:
                    resolve(prefixer.path)
                except Resolver404:
                    pass
                else:
                    return redirect(prefixer.full_path)
