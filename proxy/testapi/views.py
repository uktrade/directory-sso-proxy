from proxy.utils import BaseProxyView, CheckSignatureMixin

from django.conf import settings
from django.http import HttpResponseNotFound


class UserByEmailAPIView(CheckSignatureMixin, BaseProxyView):

    def dispatch(self, *args, **kwargs):
        if not settings.FEATURE_TEST_API_ENABLE:
            return HttpResponseNotFound()
        return super().dispatch(*args, **kwargs)
