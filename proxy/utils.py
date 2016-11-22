from hashlib import sha256
import urllib3
import urllib.parse as urlparse

from django.conf import settings
from django.utils.six.moves.urllib.parse import urlencode, quote_plus

from revproxy.views import ProxyView, QUOTE_SAFE
from revproxy.utils import encode_items


class BaseProxyView(ProxyView):

    upstream = settings.SSO_UPSTREAM

    def dispatch(self, request, *args, **kwargs):

        path = kwargs.get('path') or request.get_full_path()

        # revproxy requires the path to not start with a slash
        if path.startswith('/'):
            path = path[1:]

        return super(BaseProxyView, self).dispatch(request, path)

    def get_signature_header(self, request_url, request_payload):
        url = urlparse.urlsplit(request_url)
        path = bytes(url.path or '/', "utf-8")

        if url.query:
            path += bytes("?{}".format(url.query), "utf-8")

        salt = bytes(settings.SIGNATURE_SECRET, "utf-8")
        body = request_payload or b""

        if isinstance(body, str):
            body = bytes(body, "utf-8")

        signature = sha256(path + body + salt).hexdigest()

        return {"X-Proxy-Signature": signature}

    def _created_proxy_response(self, request, path):
        request_payload = request.body

        self.log.debug("Request headers: %s", self.request_headers)

        path = quote_plus(path.encode('utf8'), QUOTE_SAFE)

        request_url = self.get_upstream(path) + path
        self.log.debug("Request URL: %s", request_url)

        if request.GET:
            get_data = encode_items(request.GET.lists())
            request_url += '?' + urlencode(get_data)
            self.log.debug("Request URL: %s", request_url)

        try:
            signature_header = self.get_signature_header(
                request_url=request_url, request_payload=request_payload
            )
            self.request_headers = {**self.request_headers, **signature_header}

            proxy_response = self.http.urlopen(
                request.method,
                request_url,
                redirect=False,
                retries=self.retries,
                headers=self.request_headers,
                body=request_payload,
                decode_content=False,
                preload_content=False
            )
            self.log.debug("Proxy response header: %s",
                           proxy_response.getheaders())
        except urllib3.exceptions.HTTPError as error:
            self.log.exception(error)
            raise

        return proxy_response
