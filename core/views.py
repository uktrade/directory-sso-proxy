import json
import revproxy.views
import urllib3
from django.conf import settings
from django.shortcuts import redirect
from revproxy.response import get_django_response

from core import signature


class ProxyView(revproxy.views.ProxyView):
    upstream = settings.SSO_UPSTREAM
    url_prefix = ''

    def dispatch(self, request, *args, **kwargs):
        self.request_headers = self.get_request_headers()

        redirect_to = self._format_path_to_redirect(request)
        if redirect_to:
            return redirect(redirect_to)

        upstream_response = self.get_upstream_response(request)

        self._replace_host_on_redirect_location(request, upstream_response)
        self._set_content_type(request, upstream_response)

        response = get_django_response(upstream_response)

        self.log.debug('Response returned: %s', response)

        return response

    def get_upstream(self):
        return super().get_upstream(path=None)

    def get_request_headers(self):
        headers = super().get_request_headers()

        # revproxy default behaviour copies X-Forwarded-For, which we
        # don't want in order to only populate if we have both
        # X-Forwarded-For and REMOTE_ADDR to keep the number of cases we
        # _do_ populate X-Forwarded-For down
        headers.pop('X-Forwarded-For', None)

        meta = self.request.META
        meta_x_fwd_for = 'HTTP_X_FORWARDED_FOR'
        has_x_fwd_for = meta_x_fwd_for in meta
        has_remote_addr = 'REMOTE_ADDR' in meta
        if has_x_fwd_for and has_remote_addr:
            headers['X-Forwarded-For'] = meta[meta_x_fwd_for] + ', ' + self.request.META['REMOTE_ADDR']

        if not has_x_fwd_for:
            self.log.error(
                'HTTP_X_FORWARDED_FOR was missing from the request %s. '
                'This is not expected: later IP whitelisting will fail.',
                self.request,
            )
        if not has_remote_addr:
            self.log.error(
                'REMOTE_ADDR was missing from the request %s. '
                'This is not expected: later IP whitelisting will fail.',
                self.request,
            )
        headers['X-Script-Name'] = self.url_prefix
        headers['X-Forwarded-Host'] = self.request.get_host()

        return headers

    def get_upstream_response(self, request, *args, **kwargs):
        request_payload = request.body

        self.log.debug('Request headers: %s', self.request_headers)

        full_path = request.get_full_path()
        full_path = full_path.replace('/sso', '', 1)
        request_url = self.get_upstream() + full_path

        self.log.debug('Request URL: %s', request_url)

        csrf_url = self.get_upstream() + '/csrf/'

        signature_headers = signature.sso_signer.get_signature_headers(
            url=csrf_url,
            body=request_payload,
            method=request.method,
            content_type=self.request_headers.get('Content-Type'),
        )
        
        try:
            upstream_response = self.http.urlopen(
                request.method,
                csrf_url,
                redirect=False,
                retries=self.retries,
                headers={**self.request_headers, **signature_headers},
                body=request_payload,
                decode_content=False,
                preload_content=False,
            )
            self.log.debug('Proxy response header: %s', upstream_response.getheaders())
        except urllib3.exceptions.HTTPError as error:
            self.log.exception(error)
            raise
        else:
            self._replace_host_on_redirect_location(request, upstream_response)
            self._set_content_type(request, upstream_response)
            response = get_django_response(upstream_response)
            if response.status_code == 200:
                csrftoken = json.loads(response.content.decode('utf-8'))['csrftoken']
                cookies = {'Cookie': f'csrftoken={csrftoken}'}
                request_payload = request_payload.decode('ascii')
                request_payload = f'{request_payload}&csrfmiddlewaretoken={csrftoken}'
                request_payload = request_payload.encode('utf-8')
                signature_headers = signature.sso_signer.get_signature_headers(
                    url=request_url,
                    body=request_payload,
                    method=request.method,
                    content_type=self.request_headers.get('Content-Type'),
                )
                try:
                    upstream_response = self.http.urlopen(
                        request.method,
                        request_url,
                        redirect=False,
                        retries=self.retries,
                        headers={**self.request_headers, **signature_headers, **cookies},
                        body=request_payload,
                        decode_content=False,
                        preload_content=False,
                    )
                except urllib3.exceptions.HTTPError as error:
                    self.log.exception(error)
                    raise

                return upstream_response
