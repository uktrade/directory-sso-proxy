from django.http import Http404

from config import settings
from proxy.utils import BaseProxyView, CheckSignatureMixin


class UserByEmailAPIView(CheckSignatureMixin, BaseProxyView):

    def dispatch(self, *args, **kwargs):
        if not settings.TEST_API_ENABLE:
            raise Http404()
        return super().dispatch(*args, **kwargs)
