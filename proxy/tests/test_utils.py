import json
import urllib3
from unittest.mock import ANY, call, patch

import pytest

from proxy import utils


@pytest.mark.parametrize('enabled,url,expected', (
    (True, '/sso/accounts/login/', 'http://www.e.co/accounts/login/'),
    (False, '/sso/accounts/login/', 'http://www.e.co/sso/accounts/login/'),
    (True, '/accounts/login/', 'http://www.e.co/accounts/login/'),
    (False, '/accounts/login/', 'http://www.e.co/accounts/login/'),
    (
        True,
        '/sso/accounts/login/?next=/sso/accounts/logout/',
        'http://www.e.co/accounts/login/?next=/sso/accounts/logout/'
    ),

))
@patch('urllib3.poolmanager.PoolManager.urlopen')
def test_prefix_prefix(mock_urlopen, rf, settings, enabled, url, expected):
    settings.FEATURE_URL_PREFIX_ENABLED = enabled

    class TestProxyView(utils.BaseProxyView):
        upstream = 'http://www.e.co'

    mock_urlopen.return_value = urllib3.response.HTTPResponse(
        body=json.dumps({'key': 'value'}),
        headers={
            'Content-Type': 'application/json', 'Content-Length': '2'
        },
        status=200,
    )

    request = rf.get(url)
    view = TestProxyView.as_view()
    view(request)

    headers = {
        'X-Forwarded-Host': 'testserver',
        'X-Signature': ANY,
        'Cookie': ''
    }
    if enabled:
        headers['X-Script-Name'] = TestProxyView.url_prefix

    assert mock_urlopen.call_args == call(
        'GET',
        expected,
        body=b'',
        decode_content=False,
        headers=headers,
        preload_content=False,
        redirect=False,
        retries=None
    )
