from hashlib import sha256
import urllib3
import urllib.parse as urlparse

from django.conf import settings
from django.shortcuts import redirect

from revproxy.response import get_django_response
from revproxy.views import ProxyView


class BaseProxyView(ProxyView):
    upstream = settings.SSO_UPSTREAM

    def dispatch(self, request, *args, **kwargs):
        self.request_headers = self.get_request_headers()

        redirect_to = self._format_path_to_redirect(request)
        if redirect_to:
            return redirect(redirect_to)

        upstream_response = self.get_upstream_response(request)

        self._replace_host_on_redirect_location(request, upstream_response)
        self._set_content_type(request, upstream_response)

        response = get_django_response(upstream_response)

        self.log.debug("Response returned: %s", response)

        return response

    def get_signature_header(self, request_url, request_payload):
        url = urlparse.urlsplit(request_url)
        path = bytes(url.path, "utf-8")

        if url.query:
            path += bytes("?{}".format(url.query), "utf-8")

        salt = bytes(settings.SIGNATURE_SECRET, "utf-8")
        body = request_payload or b""

        if isinstance(body, str):
            body = bytes(body, "utf-8")

        signature = sha256(path + body + salt).hexdigest()

        return {"X-Proxy-Signature": signature}

    def get_upstream(self):
        return super(BaseProxyView, self).get_upstream(path=None)

    def get_upstream_response(self, request, *args, **kwargs):
        request_payload = request.body

        self.log.debug("Request headers: %s", self.request_headers)

        request_url = self.get_upstream() + request.get_full_path()

        self.log.debug("Request URL: %s", request_url)

        signature_header = self.get_signature_header(
            request_url=request_url, request_payload=request_payload
        )
        self.request_headers = {**self.request_headers, **signature_header}

        try:
            upstream_response = self.http.urlopen(
                request.method,
                request_url,
                redirect=False,
                retries=self.retries,
                headers=self.request_headers,
                body=request_payload,
                decode_content=False,
                preload_content=False
            )
            self.log.debug(
                "Proxy response header: %s",
                upstream_response.getheaders()
            )
        except urllib3.exceptions.HTTPError as error:
            self.log.exception(error)
            raise
        else:
            return upstream_response
